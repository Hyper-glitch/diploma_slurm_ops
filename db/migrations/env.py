import logging
from logging.config import fileConfig

from alembic import context
from flask import current_app
from sqlalchemy import engine_from_config, pool

config = context.config

# Interpret the config file for logging
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

config.set_main_option(
    "sqlalchemy.url",
    str(current_app.extensions["migrate"].db.get_engine().url).replace("%", "%%"),
)
target_metadata = current_app.extensions["migrate"].db.metadata


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode
    """
    connectable = config.attributes.get("connection", None)
    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
