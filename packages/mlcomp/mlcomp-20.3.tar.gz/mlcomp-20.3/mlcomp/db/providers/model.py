import datetime

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from mlcomp.db.core import PaginatorOptions
from mlcomp.db.enums import DagType
from mlcomp.db.models import Model, Dag, Project, Task
from mlcomp.db.providers.base import BaseDataProvider
from mlcomp.utils.config import Config
from mlcomp.utils.io import yaml_load
from mlcomp.utils.misc import parse_time


class ModelProvider(BaseDataProvider):
    model = Model

    def get(self, filter, options: PaginatorOptions):
        query = self.query(Model). \
            options(joinedload(Model.dag_rel, innerjoin=False)). \
            options(joinedload(Model.project_rel, innerjoin=True))

        if filter.get('project'):
            query = query.filter(Model.project == filter['project'])
        if filter.get('name'):
            query = query.filter(Model.name.like(f'%{filter["name"]}%'))

        if filter.get('created_min'):
            created_min = parse_time(filter['created_min'])
            query = query.filter(Model.created >= created_min)
        if filter.get('created_max'):
            created_max = parse_time(filter['created_max'])
            query = query.filter(Model.created <= created_max)

        total = query.count()
        paginator = self.paginator(query, options) if options else query
        res = []
        models = paginator.all()
        models_projects = set()
        for model in models:
            if not model.project_rel:
                model.project_rel = self.query(Project).filter(
                    Project.id == model.project).one()

            row = self.to_dict(model, rules=('-project_rel.class_names',))
            res.append(row)
            models_projects.add(model.project)

        last_activity = func.max(Task.last_activity).label('last_activity')
        projects = self.query(Project.name, Project.id,
                              last_activity). \
            join(Dag, Dag.project == Project.id, isouter=True). \
            join(Task, isouter=True). \
            group_by(Project.id). \
            order_by(last_activity.desc()). \
            all()
        projects = [{'name': name, 'id': id} for name, id, _ in projects]
        return {'total': total, 'data': res, 'projects': projects}

    def change_dag(self, project: int, name: str, to: int):
        ids = self.query(Model.id). \
            join(Dag). \
            filter(Model.project == project). \
            filter(Dag.name == name). \
            filter(Dag.type == DagType.Pipe.value). \
            all()

        ids = [id[0] for id in ids]

        self.query(Model). \
            filter(Model.id.in_(ids)). \
            update({'dag': to}, synchronize_session=False)
        self.commit()

    def model_start_begin(self, model_id: int):
        model = self.by_id(model_id)

        models_dags = self.query(Dag). \
            filter(Dag.type == DagType.Pipe.value). \
            filter(Dag.project == model.project). \
            order_by(Dag.id.desc()). \
            all()

        used_dag_names = set()
        versions = yaml_load(model.equations)

        res_dags = []
        res_dag = None

        for dag in models_dags:
            if dag.name in used_dag_names:
                continue
            config = Config.from_yaml(dag.config)
            d = {
                'name': dag.name,
                'id': dag.id,
                'pipes': [{
                    'name': p
                } for p in config['pipes']]
            }
            for pipe in d['pipes']:
                pipe['versions'] = versions.get(pipe['name'], [])
                used = [v.get('used', datetime.datetime.min) for v in
                        pipe['versions']]
                pipe['used'] = datetime.datetime.min if len(
                    used) == 0 else max(used)

            d['pipes'] = sorted(d['pipes'], key=lambda x: x['used'],
                                reverse=True)
            for p in d['pipes']:
                del p['used']
                for v in p['versions']:
                    if 'used' in v:
                        del v['used']

            used_dag_names.add(dag.name)
            res_dags.append(d)

            if d['id'] == model.dag:
                res_dag = d

        return {'dags': res_dags, 'dag': res_dag, 'model_id': model_id}


__all__ = ['ModelProvider']
