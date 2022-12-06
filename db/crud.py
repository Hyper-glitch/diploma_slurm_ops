from sqlalchemy.orm import Session

from . import schemas
from .models import Dimension, Resource, Team


def get_dimension(session: Session, dimension_id: int):
    return session.query(Dimension).filter_by(id=dimension_id).one_or_none()


def get_resource(session: Session, resource_id: int):
    return session.query(Resource).filter_by(id=resource_id).one_or_none()


def get_team(session: Session, team_id: int):
    return session.query(Team).filter_by(id=team_id).one_or_none()


def create_dimension(session: Session, dimension: schemas.Dimension, resource_id: int):
    db_dimension = Dimension(**dimension.dict(), resource_id=resource_id)
    session.add(db_dimension)
    session.commit()
    session.refresh(db_dimension)
    return db_dimension


def create_resource(session: Session, resource: schemas.Resource, team_id: int):
    db_resource = Resource(**resource.dict(), team_id=team_id)
    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource


def create_team(session: Session, team: schemas.Team):
    db_team = Team(**team.dict())
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team
