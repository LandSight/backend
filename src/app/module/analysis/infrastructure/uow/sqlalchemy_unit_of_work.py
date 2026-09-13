"""SQLAlchemy unit of work implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import UnitOfWork


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUnitOfWork(UnitOfWork):
    """Unit of work backed by an async SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def commit(self) -> None:
        """See :class:`app.module.analysis.application.port.UnitOfWork.commit`."""
        await self._session.commit()

    @override
    async def rollback(self) -> None:
        """See :class:`app.module.analysis.application.port.UnitOfWork.rollback`."""
        await self._session.rollback()


__all__ = ("SqlAlchemyUnitOfWork",)
