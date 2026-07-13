"""Alembic environment configuration for Platform-level migrations."""

import asyncio
from typing import TYPE_CHECKING

from alembic import context


if TYPE_CHECKING:
    from sqlalchemy.engine import Connection

from app.platform.config.loaders import load_app_config
from app.platform.database.engine import create_async_engine_from_config, dispose_engine
from app.platform.logging import configure_logging


config = context.config
app_config = load_app_config()

configure_logging(app_config.logging)

# Import all models so that Alembic can detect them for autogenerate.
from app.platform.database.base import BaseModel  # noqa: E402


target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=app_config.database.get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with a given connection."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with an async engine."""
    engine = create_async_engine_from_config(app_config.database)

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await dispose_engine(engine)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
