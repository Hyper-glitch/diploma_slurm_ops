"""Module for set up metrics generator environment vars."""
from environs import Env

env = Env()
env.read_env()

METRICS_GEN_SERVICE_PORT = env.int("MONITORING_SERVICE_PORT", 21122)
METRICS_GEN_SERVICE_HOST = env.str("MONITORING_SERVICE_HOST", "localhost")
