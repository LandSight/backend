"""Alembic environment configuration for all module migrations.

This single ``env.py`` is shared across all modules (platform, identity, parcel, topography).
It detects which module is being targeted via the ``-n`` flag (``config.config_ini_section``)
and dynamically imports the appropriate models for autogenerate support.

Usage
-----
    alembic -n platform revision --autogenerate -m "..."
    alembic -n identity revision --autogenerate -m "..."
    alembic -n parcel revision --autogenerate -m "..."
    alembic -n topography revision --autogenerate -m "..."
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from alembic import context
from sqlalchemy import Table, text


if TYPE_CHECKING:
    from sqlalchemy.engine import Connection

from app.platform.config.loaders import load_app_config
from app.platform.database.engine import create_async_engine_from_config, dispose_engine
from app.platform.logging import configure_logging


config = context.config
app_config = load_app_config()

configure_logging(app_config.logging)

# Detect which module is being targeted via the -n flag.
# config.config_ini_section returns the section name (e.g. "identity", "parcel").
service: str = config.config_ini_section

# Dynamically import models based on the target module.
# Upstream modules must be imported so that Alembic can resolve FK chains.
if service == "platform":
    from app.platform.database.base import BaseModel

    target_metadata = BaseModel.metadata
    version_table_schema: str | None = None
    schema_name: str | None = None
    # Platform migrations have no schema filter.
    include_schema: str | None = None

elif service == "identity":
    from app.platform.database.base import BaseModel

    target_metadata = BaseModel.metadata
    version_table_schema = "identity"
    schema_name = "identity"
    include_schema = "identity"

elif service == "parcel":
    # Parcel FK: parcels.owner_id -> identity.users.id
    from app.platform.database.base import BaseModel

    target_metadata = BaseModel.metadata
    version_table_schema = "parcel"
    schema_name = "parcel"
    include_schema = "parcel"

elif service == "topography":
    # Topography FK: metrics.parcel_id -> parcel.parcels.id
    # Parcel FK: parcels.owner_id -> identity.users.id
    from app.platform.database.base import BaseModel

    target_metadata = BaseModel.metadata
    version_table_schema = "topography"
    schema_name = "topography"
    include_schema = "topography"

else:
    message = f"Unknown Alembic service target: '{service}'. Expected one of: platform, identity, parcel, topography."
    raise ValueError(message)


def include_object(
    obj: object,
    _name: str,
    type_: str,
    _reflected: bool,
    _compare_to: object,
) -> bool:
    """Filter objects to only include those in the target module's schema.

    This prevents Alembic autogenerate from detecting tables belonging to
    other modules (which are imported only for FK resolution).
    """
    if type_ == "table" and include_schema is not None:
        if isinstance(obj, Table):
            return obj.schema == include_schema
        return False
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    kwargs: dict = {
        "url": app_config.database.get_url(),
        "target_metadata": target_metadata,
        "literal_binds": True,
        "dialect_opts": {"paramstyle": "named"},
    }
    if version_table_schema:
        kwargs["version_table_schema"] = version_table_schema
    if include_schema:
        kwargs["include_object"] = include_object
        kwargs["include_schemas"] = True

    context.configure(**kwargs)

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with a given connection."""
    kwargs: dict = {
        "connection": connection,
        "target_metadata": target_metadata,
    }
    if version_table_schema:
        kwargs["version_table_schema"] = version_table_schema
    if include_schema:
        kwargs["include_object"] = include_object
        kwargs["include_schemas"] = True

    context.configure(**kwargs)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with an async engine."""
    engine = create_async_engine_from_config(app_config.database)

    async with engine.connect() as connection:
        # Ensure the schema exists before Alembic tries to write version_table there.
        # Must be outside Alembic's transaction to avoid DDL conflicts.
        if schema_name:
            await connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
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
