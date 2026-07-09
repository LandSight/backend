"""Litestar dependency providers for platform-level dependencies."""

from __future__ import annotations

from typing import TYPE_CHECKING

from litestar.di import NamedDependency, Provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from app.platform.config.loaders import load_auth_config, load_database_config
from app.platform.config.models import AuthConfig, DatabaseConfig
from app.platform.database.engine import create_async_engine_from_config
from app.platform.database.session import create_async_session_factory, get_async_session


# ----- Configs -----
async def provide_database_config() -> DatabaseConfig:
    """Provide database configuration."""
    return load_database_config()


async def provide_auth_config() -> AuthConfig:
    """Provide authentication configuration."""
    return load_auth_config()


# ----- Engine -----
async def provide_async_database_engine(
    database_config: NamedDependency[DatabaseConfig],
) -> AsyncEngine:
    """Provide async database engine."""
    return create_async_engine_from_config(database_config)


# ----- Session -----
async def provide_async_session_factory(
    database_engine: NamedDependency[AsyncEngine],
) -> async_sessionmaker[AsyncSession]:
    """Provide a session factory bound to the engine."""
    return create_async_session_factory(database_engine)


async def provide_async_session(
    session_factory: NamedDependency[async_sessionmaker[AsyncSession]],
) -> AsyncGenerator[AsyncSession]:
    """Provide a new async session per request.

    The session is closed automatically after the request finishes.
    """
    async with get_async_session(session_factory) as session:
        yield session


platform_dependencies = {
    "database_config": Provide(provide_database_config, use_cache=True),
    "auth_config": Provide(provide_auth_config, use_cache=True),
    "database_engine": Provide(provide_async_database_engine, use_cache=True),
    "session_factory": Provide(provide_async_session_factory),
    "session": Provide(provide_async_session),
}


__all__ = (
    "platform_dependencies",
    "provide_async_session",
    "provide_auth_config",
)
