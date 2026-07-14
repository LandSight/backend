"""Base repository with session access."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class BaseSQLAlchemyRepository:
    """Base repository that holds an async session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session


__all__ = ("BaseSQLAlchemyRepository",)
