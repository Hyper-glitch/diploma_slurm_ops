import logging
import os

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource as otl_resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from analyze_service.analyzer import handle_raw_data
from api.coroutine.resource import get_resource_task
from api.dto.metrics import TeamDTO, TeamsDTO
from span import SpanFormatter
from sql_app import models, schemas, crud
from sql_app.database import engine, get_db
from sql_app.schemas import Team, Resource, Dimension

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

AGENT_HOSTNAME = os.getenv("AGENT_HOSTNAME", "localhost")
AGENT_PORT = int(os.getenv("AGENT_PORT", "4317"))


resource = otl_resource(attributes={
    "service.name": "service-api"
})
trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint=f"{AGENT_HOSTNAME}:{AGENT_PORT}", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
FastAPIInstrumentor.instrument_app(app)


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(SpanFormatter(
         'time="%(asctime)s" service=%(name)s level=%(levelname)s %(message)s trace_id=%(trace_id)s'
     ))
    logger.addHandler(handler)


@app.get("/analyzed_metrics/{portion_amount}")
async def read_analyzed_metrics(portion_amount: int) -> dict[str, TeamsDTO]:
    raw_data = await get_resource_task(portion_amount=portion_amount)
    teams_dto: list[TeamDTO] = []

    for data in raw_data:
        teams_dto.extend(TeamsDTO.prepare_teams_dto(data=handle_raw_data(data)))
    response = TeamsDTO(teams=teams_dto)

    return {"analyzed_data": response}


@app.post("/teams/", response_model=schemas.Team)
async def add_teams(team: Team, db=Depends(get_db)):
    db_team = crud.get_team(db=db, team_id=team.id)
    if db_team:
        raise HTTPException(status_code=400, detail="Team has already exists")
    return crud.create_team(db=db, team=team)


@app.post("/resources/", response_model=schemas.Resource)
async def add_teams(resource: Resource, db=Depends(get_db)):
    db_resource = crud.get_resource(db=db, resource_id=resource.id)
    if db_resource:
        raise HTTPException(status_code=400, detail="Resource has already exists")
    return crud.create_resource(db=db, resource=resource, team_id=resource.team_id)


@app.post("/dimensions/", response_model=schemas.Dimension)
async def add_teams(dimension: Dimension, db=Depends(get_db)):
    db_resource = crud.get_dimension(db=db, dimension_id=dimension.id)
    if db_resource:
        raise HTTPException(status_code=400, detail="Dimension has already exists")
    return crud.create_dimension(db=db, dimension=dimension, resource_id=dimension.resource_id)


if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, log_level="info")
