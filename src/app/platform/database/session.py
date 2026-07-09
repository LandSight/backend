from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)


def create_async_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create an async session factory.

    Parameters
    ----------
    engine : AsyncEngine
        Database engine.

    Returns
    -------
    async_sessionmaker[AsyncSession]
        Session factory.
    """
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@asynccontextmanager
async def get_async_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    """Get a database session with automatic commit/rollback.

    Parameters
    ----------
    session_factory : async_sessionmaker[AsyncSession]
        Session factory.

    Yields
    ------
    AsyncSession
        Database session.
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


__all__ = (
    "create_async_session_factory",
    "get_async_session",
)
