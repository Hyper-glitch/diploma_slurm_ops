import asyncio
import logging
import sys
from typing import Union

from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from analyze_service.analyzer import handle_raw_data
from api.coroutine.metrics import get_resource_task
from api.dto.metrics import AnalyzedMetricsDTO, TeamDTO, TeamsDTO

logger = logging.getLogger('trello_creator')
app = FastAPI()


def set_up_logger():
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
    logger.addHandler(handler)


@app.get("/analyzed_metrics/{portion_amount}")
async def read_analyzed_metrics(portion_amount: int) -> dict[str, TeamsDTO]:
    raw_data = await get_resource_task(portion_amount=portion_amount)
    teams_dto: list[TeamDTO] = []

    for data in raw_data:
        teams_dto.extend(AnalyzedMetricsDTO.prepare_nested_dto(data=handle_raw_data(data)))
    response = TeamsDTO(teams=teams_dto)

    return {"analyzed_data": response}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    set_up_logger()
    FastAPIInstrumentor.instrument_app(app)
    asyncio.run(serve(app, Config()))
