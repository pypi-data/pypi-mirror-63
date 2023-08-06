import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from mlcomp.db.models.base import Base


class Model(Base):
    __tablename__ = 'model'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    score_local = sa.Column(sa.Float)
    score_public = sa.Column(sa.Float)
    project = sa.Column(sa.Integer, ForeignKey('project.id'))
    dag = sa.Column(sa.Integer, ForeignKey('dag.id'))
    created = sa.Column(sa.DateTime)
    equations = sa.Column(sa.String)
    fold = sa.Column(sa.Integer)

    dag_rel = relationship('Dag', lazy='noload')
    project_rel = relationship('Project', lazy='noload')


__all__ = ['Model']
