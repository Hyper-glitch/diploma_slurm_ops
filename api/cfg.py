"""Module for set up api environment vars."""
from environs import Env

env = Env()
env.read_env()

METRICS_GEN_SERVICE_PORT = env.int("MONITORING_SERVICE_PORT", 21122)
METRICS_GEN_SERVICE_HOST = env.str("MONITORING_SERVICE_HOST", "metrics_generator")
METRICS_GEN_SERVICE_ENDPOINT = env.str("MONITORING_SERVICE_HOST", "generate_metrics")
OTLP_EXPORTER_AGENT_HOSTNAME = env.str("OTLP_EXPORTER_AGENT_HOSTNAME", "otel-collector")
OTLP_EXPORTER_AGENT_PORT = env.int("OTLP_EXPORTER_AGENT_PORT", "4317")
