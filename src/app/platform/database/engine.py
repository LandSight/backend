"""Database engine and session factory."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)


if TYPE_CHECKING:
    from app.platform.config.models import DatabaseConfig


def create_async_engine_from_config(config: DatabaseConfig) -> AsyncEngine:
    """Create an async database engine.

    Parameters
    ----------
    config : DatabaseConfig
        Database configuration.

    Returns
    -------
    AsyncEngine
        Configured async engine.
    """
    return create_async_engine(
        config.get_url(),
        echo=config.echo,
        pool_size=config.pool_size,
        max_overflow=config.max_overflow,
    )


async def dispose_engine(engine: AsyncEngine) -> None:
    """Dispose of an async database engine, closing all connections.

    Parameters
    ----------
    engine : AsyncEngine
        Database engine to dispose.
    """
    await engine.dispose()


__all__ = (
    "create_async_engine_from_config",
    "dispose_engine",
)
