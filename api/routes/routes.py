from fastapi import APIRouter, Depends, HTTPException

from analyze_service.analyzer import handle_raw_data
from api.coroutine.resource import get_resource_task
from api.dto.metrics import TeamsResponse, TeamResponse
from db import schemas, crud
from db.database import get_session
from db.schemas import Team, Resource, Dimension

router = APIRouter()


@router.get("/analyzed_metrics/{portion_amount}")
async def read_analyzed_metrics(portion_amount: int) -> dict[str, TeamsResponse]:
    raw_data = await get_resource_task(portion_amount=portion_amount)
    teams_dto: list[TeamResponse] = []

    for data in raw_data:
        teams_dto.extend(TeamsResponse.prepare_teams_dto(data=handle_raw_data(data)))
    response = TeamsResponse(teams=teams_dto)

    return {"analyzed_data": response}


@router.post("/teams/", response_model=schemas.Team)
async def add_teams(team: Team, session=Depends(get_session)):
    db_team = crud.get_team(session=session, team_id=team.id)
    if db_team:
        raise HTTPException(status_code=400, detail="Team has already exists")
    return crud.create_team(session=session, team=team)


@router.post("/resources/", response_model=schemas.Resource)
async def add_teams(resource: Resource, session=Depends(get_session)):
    db_resource = crud.get_resource(session=session, resource_id=resource.id)
    if db_resource:
        raise HTTPException(status_code=400, detail="Resource has already exists")
    return crud.create_resource(session=session, resource=resource, team_id=resource.team_id)


@router.post("/dimensions/", response_model=schemas.Dimension)
async def add_teams(dimension: Dimension, session=Depends(get_session)):
    db_resource = crud.get_dimension(session=session, dimension_id=dimension.id)
    if db_resource:
        raise HTTPException(status_code=400, detail="Dimension has already exists")
    return crud.create_dimension(session=session, dimension=dimension, resource_id=dimension.resource_id)
