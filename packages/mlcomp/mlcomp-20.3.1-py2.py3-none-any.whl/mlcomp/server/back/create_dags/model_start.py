from mlcomp.db.core import Session
from mlcomp.db.models import Dag
from mlcomp.db.providers import ModelProvider, DagProvider
from mlcomp.server.back.create_dags.standard import dag_standard
from mlcomp.utils.config import Config
from mlcomp.utils.io import yaml_load, yaml_dump
from mlcomp.utils.misc import now


def dag_model_start(session: Session, data: dict):
    provider = ModelProvider(session)
    model = provider.by_id(data['model_id'])
    dag_provider = DagProvider(session)
    dag = dag_provider.by_id(data['dag'], joined_load=[Dag.project_rel])

    project = dag.project_rel
    src_config = Config.from_yaml(dag.config)
    pipe = src_config['pipes'][data['pipe']['name']]

    equations = yaml_load(model.equations)
    versions = data['pipe']['versions']

    if len(versions) > 0:
        version = data['pipe']['version']
        pipe_equations = yaml_load(version['equations'])
        found_version = versions[0]
        for v in versions:
            if v['name'] == version['name']:
                found_version = v
                break

        found_version['used'] = now()

        for v in pipe.values():
            v.update(pipe_equations)

    equations[data['pipe']['name']] = versions
    model.equations = yaml_dump(equations)

    for v in pipe.values():
        v['model_id'] = model.id
        v['model_name'] = model.name

    config = {
        'info': {
            'name': data['pipe']['name'],
            'project': project.name
        },
        'executors': pipe
    }

    if model.dag:
        old_dag = dag_provider.by_id(model.dag)
        if old_dag.name != dag.name:
            model.dag = dag.id
    else:
        model.dag = dag.id

    provider.commit()

    dag_standard(
        session=session,
        config=config,
        debug=False,
        upload_files=False,
        copy_files_from=data['dag']
    )


__all__ = ['dag_model_start']
