import asyncio
import logging
import sys
from typing import Union

from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from metrics_generator.utils import task

logger = logging.getLogger('trello_creator')
app = FastAPI()


def set_up_logger():
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
    logger.addHandler(handler)


@app.get("/analyzed_metrics")
async def read_analyzed_metrics():
    analyzed_data = await task()
    return {"analyzed_data": analyzed_data}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    set_up_logger()
    FastAPIInstrumentor.instrument_app(app)
    asyncio.run(serve(app, Config()))
