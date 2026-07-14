"""Litestar dependency providers for platform-level dependencies."""

from __future__ import annotations

from typing import TYPE_CHECKING

from litestar.datastructures import State
from litestar.di import NamedDependency, Provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


from app.platform.config.loaders import load_auth_config, load_database_config
from app.platform.config.models import AuthConfig, DatabaseConfig
from app.platform.database.session import create_async_session_factory


# ----- Configs -----
def provide_database_config() -> DatabaseConfig:
    """Provide database configuration."""
    return load_database_config()


def provide_auth_config() -> AuthConfig:
    """Provide authentication configuration."""
    return load_auth_config()


# ----- Session -----
def provide_async_session_factory(
    state: State,
) -> async_sessionmaker[AsyncSession]:
    """Provide a session factory bound to the app database engine."""
    return create_async_session_factory(state.engine)


async def provide_async_session(
    session_factory: NamedDependency[async_sessionmaker[AsyncSession]],
) -> AsyncGenerator[AsyncSession]:
    """Provide a new async session per request.

    The session is closed automatically after the request finishes.
    """
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


platform_dependencies = {
    "database_config": Provide(provide_database_config, use_cache=True),
    "auth_config": Provide(provide_auth_config, use_cache=True),
    "session_factory": Provide(provide_async_session_factory, use_cache=True),
    "session": Provide(provide_async_session),
}


__all__ = (
    "platform_dependencies",
    "provide_async_session",
    "provide_auth_config",
)
