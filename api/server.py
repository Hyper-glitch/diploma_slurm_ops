import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from api.cfg import OTLP_EXPORTER_AGENT_HOSTNAME, OTLP_EXPORTER_AGENT_PORT
from api.routes.routes import router
from db import cfg
from db import tasks
from db.database import engine
from span import SpanFormatter


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
    resource = Resource(attributes={"service.name": "service-async_analyze_metrics"})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    otlp_exporter = OTLPSpanExporter(
        endpoint=f"{OTLP_EXPORTER_AGENT_HOSTNAME}:{OTLP_EXPORTER_AGENT_PORT}",
        insecure=True,
    )
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument(engine=engine)
    return app


app = get_application()


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(
        SpanFormatter(
            'time="%(asctime)s" service=%(name)s level=%(levelname)s %(message)s trace_id=%(trace_id)s'
        )
    )
    logger.addHandler(handler)
