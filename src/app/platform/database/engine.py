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
        config.url,
        echo=config.echo,
        pool_size=config.pool_size,
        max_overflow=config.max_overflow,
    )


__all__ = ("create_async_engine_from_config",)
