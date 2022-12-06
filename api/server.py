import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.routes import router
from span import SpanFormatter
from db import cfg
from db import tasks


def get_application():
    app = FastAPI(title=cfg.PROJECT_NAME, version=cfg.VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))
    app.include_router(router, prefix="/api")

    return app


app = get_application()


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(SpanFormatter(
        'time="%(asctime)s" service=%(name)s level=%(levelname)s %(message)s trace_id=%(trace_id)s'
    ))
    logger.addHandler(handler)
