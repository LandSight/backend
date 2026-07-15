"""Alembic environment configuration for Parcel module migrations."""

import asyncio
from typing import TYPE_CHECKING

from alembic import context
from sqlalchemy import text


if TYPE_CHECKING:
    from sqlalchemy.engine import Connection

from app.platform.config.loaders import load_app_config
from app.platform.database.engine import create_async_engine_from_config, dispose_engine
from app.platform.logging import configure_logging


config = context.config
app_config = load_app_config()

configure_logging(app_config.logging)

# Import all models so that Alembic can detect them for autogenerate.
# Identity model is imported so that Alembic can resolve the FK to identity.users.
import app.module.identity.infrastructure.model  # noqa: E402
import app.module.parcel.infrastructure.model  # noqa: F401, E402
from app.platform.database.base import BaseModel  # noqa: E402


# Set target metadata for autogenerate support.
target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=app_config.database.get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema="parcel",
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with a given connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema="parcel",
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with an async engine."""
    engine = create_async_engine_from_config(app_config.database)

    async with engine.connect() as connection:
        # Ensure the schema exists before Alembic tries to write version_table there.
        # Must be outside Alembic's transaction to avoid DDL conflicts.
        await connection.execute(text("CREATE SCHEMA IF NOT EXISTS parcel"))
        await connection.commit()
        await connection.run_sync(do_run_migrations)

    await dispose_engine(engine)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
