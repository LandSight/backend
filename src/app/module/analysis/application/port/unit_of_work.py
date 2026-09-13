"""Unit of work port."""

from __future__ import annotations

from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    """Port for controlling transaction boundaries inside use cases.

    Implementations:
    - :class:`app.module.analysis.infrastructure.uow.sqlalchemy_unit_of_work.SqlAlchemyUnitOfWork`
    """

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Roll back the current transaction."""
        raise NotImplementedError


__all__ = ("UnitOfWork",)
