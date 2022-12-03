"""Module for set up environment vars."""
from environs import Env

env = Env()
env.read_env()

MONITORING_SERVICE_PORT = env.int('MONITORING_SERVICE_PORT', 21122)
MONITORING_SERVICE_HOST = env.str('MONITORING_SERVICE_HOST', 'localhost')

# DB_PSQL = env.str('DB_PSQL')
# DB_USER_PSQL = env.str('DB_USER_PSQL')
# DB_PASS_PSQL = env.str('DB_PASS_PSQL')
# DB_HOST_PSQL = env.str('DB_HOST_PSQL', 'localhost')
# DB_PORT_PSQL = env.int('DB_PORT_PSQL', 5432)
# DB_SCHEMA_PSQL = env.str('DB_SCHEMA_PSQL')
