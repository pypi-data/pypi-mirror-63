import os
import socket
from collections import OrderedDict
from pathlib import Path
from os.path import join

import torch

from catalyst.utils import set_global_seed, \
    import_experiment_and_runner, parse_args_uargs, dump_environment, \
    load_checkpoint
from catalyst.dl import State, Callback, Runner, CheckpointCallback

from mlcomp import TASK_FOLDER
from mlcomp.db.providers import ReportSeriesProvider, ComputerProvider
from mlcomp.db.report_info import ReportLayoutInfo
from mlcomp.utils.io import yaml_load, yaml_dump
from mlcomp.utils.misc import now
from mlcomp.db.models import ReportSeries
from mlcomp.utils.config import Config, merge_dicts_smart
from mlcomp.worker.executors.base import Executor
from mlcomp.worker.executors.model import trace_model_from_checkpoint
from mlcomp.worker.sync import copy_remote


class Args:
    baselogdir = None
    batch_size = None
    check = False
    config = None
    configs = []
    expdir = None
    logdir = None
    num_epochs = None
    num_workers = None
    resume = None
    seed = 42
    verbose = True

    def _get_kwargs(self):
        return [
            (k, v) for k, v in self.__dict__.items() if not k.startswith('_')
        ]


# noinspection PyTypeChecker
@Executor.register
class Catalyst(Executor, Callback):
    def __init__(
            self,
            args: Args,
            report: ReportLayoutInfo,
            distr_info: dict,
            resume: dict,
            grid_config: dict,
            trace: str,
            params: dict,
            **kwargs
    ):
        super().__init__(**kwargs)

        self.series_provider = ReportSeriesProvider(self.session)
        self.computer_provider = ComputerProvider(self.session)

        self.order = 0
        self.resume = resume
        self.distr_info = distr_info
        self.args = args
        self.report = report
        self.experiment = None
        self.runner = None
        self.grid_config = grid_config
        self.master = True
        self.trace = trace
        self.params = params
        self.last_batch_logged = None
        self.loader_started_time = None
        self.parent = None

    def get_parent_task(self):
        if self.parent:
            return self.parent
        return self.task

    def callbacks(self):
        result = OrderedDict()
        if self.master:
            result['catalyst'] = self

        return result

    def on_loader_start(self, state: State):
        self.loader_started_time = now()

    def on_epoch_start(self, state: State):
        stage_index = self.experiment.stages.index(state.stage_name)
        self.step.start(1, name=state.stage_name, index=stage_index)

        self.step.start(
            2, name=f'epoch {state.epoch}', index=state.epoch - 1
        )

    def on_batch_start(self, state: State):
        if self.last_batch_logged and state.loader_step != state.loader_len:
            if (now() - self.last_batch_logged).total_seconds() < 10:
                return

        task = self.get_parent_task()
        task.batch_index = state.loader_step
        task.batch_total = state.loader_len
        task.loader_name = state.loader_name

        duration = int((now() - self.loader_started_time).total_seconds())
        task.epoch_duration = duration
        task.epoch_time_remaining = int(duration * (
                task.batch_total / task.batch_index)) - task.epoch_duration
        if state.loader_metrics.get('loss') is not None:
            task.loss = float(state.loader_metrics['loss'])

        self.task_provider.update()
        self.last_batch_logged = now()

    def on_epoch_end(self, state: State):
        self.step.end(2)

        values = state.epoch_metrics

        for k, v in values.items():
            part = ''
            name = k

            for loader in state.loaders:
                if k.startswith(loader):
                    part = loader
                    name = k.replace(loader, '')
                    if name.startswith('_'):
                        name = name[1:]

            task_id = self.task.parent or self.task.id
            series = ReportSeries(
                part=part,
                name=name,
                epoch=state.epoch - 1,
                task=task_id,
                value=v,
                time=now(),
                stage=state.stage_name
            )
            self.series_provider.add(series)

            if name == self.report.metric.name:
                best = False
                task = self.task
                if task.parent:
                    task = self.task_provider.by_id(task.parent)

                if self.report.metric.minimize:
                    if task.score is None or v < task.score:
                        best = True
                else:
                    if task.score is None or v > task.score:
                        best = True
                if best:
                    task.score = v
                    self.task_provider.update()

    def on_stage_end(self, state: State):
        self.step.end(1)

    @classmethod
    def _from_config(
            cls, executor: dict, config: Config, additional_info: dict
    ):
        args = Args()
        for k, v in executor['args'].items():
            v = str(v)
            if v in ['False', 'True']:
                v = v == 'True'
            elif v.isnumeric():
                v = int(v)

            setattr(args, k, v)

        assert 'report_config' in additional_info, 'layout was not filled'
        report_config = additional_info['report_config']
        report = ReportLayoutInfo(report_config)
        if len(args.configs) == 0:
            args.configs = [args.config]

        distr_info = additional_info.get('distr_info', {})
        resume = additional_info.get('resume')
        params = executor.get('params', {})
        params.update(additional_info.get('params', {}))

        grid_config = executor.copy()
        grid_config.pop('args', '')

        return cls(
            args=args,
            report=report,
            grid_config=grid_config,
            distr_info=distr_info,
            resume=resume,
            trace=executor.get('trace'),
            params=params
        )

    def set_dist_env(self, config):
        info = self.distr_info
        os.environ['MASTER_ADDR'] = info['master_addr']
        os.environ['MASTER_PORT'] = str(info['master_port'])
        os.environ['WORLD_SIZE'] = str(info['world_size'])

        os.environ['RANK'] = str(info['rank'])
        distributed_params = config.get('distributed_params', {})
        distributed_params['rank'] = info['rank']
        config['distributed_params'] = distributed_params

        if info['rank'] > 0:
            self.master = False

    def parse_args_uargs(self):
        args, config = parse_args_uargs(self.args, [])
        config = merge_dicts_smart(config, self.grid_config)
        config = merge_dicts_smart(config, self.params)

        if self.distr_info:
            self.set_dist_env(config)
        return args, config

    def _checkpoint_fix_config(self, experiment):
        resume = self.resume
        if not resume:
            return
        if experiment.logdir is None:
            return

        checkpoint_dir = join(experiment.logdir, 'checkpoints')
        os.makedirs(checkpoint_dir, exist_ok=True)

        file = 'last_full.pth' if resume.get('load_last') else 'best_full.pth'

        path = join(checkpoint_dir, file)
        computer = socket.gethostname()
        if computer != resume['master_computer']:
            master_computer = self.computer_provider.by_name(
                resume['master_computer'])
            path_from = join(
                master_computer.root_folder, str(resume['master_task_id']),
                experiment.logdir,
                'checkpoints', file
            )
            self.info(
                f'copying checkpoint from: computer = '
                f'{resume["master_computer"]} path_from={path_from} '
                f'path_to={path}'
            )

            success = copy_remote(
                session=self.session,
                computer_from=resume['master_computer'],
                path_from=path_from,
                path_to=path
            )

            if not success:
                self.error(
                    f'copying from '
                    f'{resume["master_computer"]}/'
                    f'{path_from} failed'
                )
            else:
                self.info('checkpoint copied successfully')

        elif self.task.id != resume['master_task_id']:
            path = join(
                TASK_FOLDER, str(resume['master_task_id']), experiment.logdir,
                'checkpoints', file
            )
            self.info(
                f'master_task_id!=task.id, using checkpoint'
                f' from task_id = {resume["master_task_id"]}'
            )

        if not os.path.exists(path):
            self.info(f'no checkpoint at {path}')
            return

        ckpt = load_checkpoint(path)
        stages_config = experiment.stages_config
        for k, v in list(stages_config.items()):
            if k == ckpt['stage']:
                stage_epoch = ckpt['checkpoint_data']['epoch'] + 1

                # if it is the last epoch in the stage
                if stage_epoch >= v['state_params']['num_epochs'] \
                        or resume.get('load_best'):
                    del stages_config[k]
                    break

                self.checkpoint_stage_epoch = stage_epoch
                v['state_params']['num_epochs'] -= stage_epoch
                break
            del stages_config[k]

        stage = experiment.stages_config[experiment.stages[0]]
        for k, v in stage['callbacks_params'].items():
            if v.get('callback') == 'CheckpointCallback':
                v['resume'] = path

        self.info(f'found checkpoint at {path}')

    def _checkpoint_fix_callback(self, callbacks: dict):
        def mock(state):
            pass

        for k, c in callbacks.items():
            if not isinstance(c, CheckpointCallback):
                continue

            if c.resume:
                self.checkpoint_resume = True

            if not self.master:
                c.on_epoch_end = mock
                c.on_stage_end = mock
                c.on_batch_start = mock

    def work(self):
        args, config = self.parse_args_uargs()
        set_global_seed(args.seed)

        Experiment, R = import_experiment_and_runner(Path(args.expdir))

        runner_params = config.pop('runner_params', {})

        experiment = Experiment(config)
        runner: Runner = R(**runner_params)

        self.experiment = experiment
        self.runner = runner

        stages = experiment.stages[:]

        if self.task.parent:
            self.parent = self.task_provider.by_id(self.task.parent)

        if self.master:
            task = self.get_parent_task()
            task.steps = len(stages)
            self.task_provider.commit()

        self._checkpoint_fix_config(experiment)

        _get_callbacks = experiment.get_callbacks

        def get_callbacks(stage):
            res = self.callbacks()
            for k, v in _get_callbacks(stage).items():
                res[k] = v

            self._checkpoint_fix_callback(res)
            return res

        experiment.get_callbacks = get_callbacks

        if experiment.logdir is not None:
            dump_environment(config, experiment.logdir, args.configs)

        if self.distr_info:
            info = yaml_load(self.task.additional_info)
            info['resume'] = {
                'master_computer': self.distr_info['master_computer'],
                'master_task_id': self.task.id - self.distr_info['rank'],
                'load_best': True
            }
            self.task.additional_info = yaml_dump(info)
            self.task_provider.commit()

            experiment.stages_config = {
                k: v
                for k, v in experiment.stages_config.items()
                if k == experiment.stages[0]
            }

        runner.run_experiment(experiment)
        if runner.state.exception:
            raise runner.state.exception

        if self.master and self.trace:
            traced = trace_model_from_checkpoint(self.experiment.logdir, self)
            torch.jit.save(traced, self.trace)
        return {'stage': experiment.stages[-1], 'stages': stages}


__all__ = ['Catalyst']
