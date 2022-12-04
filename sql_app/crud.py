from sqlalchemy.orm import Session

from . import schemas
from .models import Dimension, Resource, Team


def get_dimension(db: Session, dimension_id: int):
    return db.query(Dimension).filter_by(id=dimension_id).one_or_none()


def get_resource(db: Session, resource_id: int):
    return db.query(Resource).filter_by(id=resource_id).one_or_none()


def get_team(db: Session, team_id: int):
    return db.query(Team).filter_by(id=team_id).one_or_none()


def create_dimension(db: Session, dimension: schemas.Dimension, resource_id: int):
    db_dimension = Dimension(**dimension.dict(), resource_id=resource_id)
    db.add(db_dimension)
    db.commit()
    db.refresh(db_dimension)
    return db_dimension


def create_resource(db: Session, resource: schemas.Resource, team_id: int):
    db_resource = Resource(**resource.dict(), team_id=team_id)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


def create_team(db: Session, team: schemas.Team):
    db_team = Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team
