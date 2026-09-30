"""Outbox repository port and PostgreSQL implementation."""

from __future__ import annotations

import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from sqlalchemy import select, update

from app.platform.database.repository import BaseSQLAlchemyRepository
from app.platform.outbox.models import OutboxEventModel


if TYPE_CHECKING:
    from collections.abc import Mapping
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True, slots=True)
class OutboxEvent:
    """A pending outbox event read by the relay.

    Attributes
    ----------
    id : UUID
        Event identifier.
    event_type : str
        Dotted event type.
    payload : Mapping[str, object]
        Self-contained event payload.
    """

    id: UUID
    event_type: str
    payload: Mapping[str, object]


class OutboxRepository(ABC):
    """Port for reading and writing outbox events.

    Implementations:
    - :class:`app.platform.outbox.repository.PostgresOutboxRepository`
    """

    @abstractmethod
    async def append(self, event_type: str, payload: Mapping[str, object]) -> None:
        """Append an event to the outbox within the caller's transaction."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_pending(self, limit: int) -> list[OutboxEvent]:
        """Lock and return pending events that have not exhausted their attempts."""
        raise NotImplementedError

    @abstractmethod
    async def mark_published(self, event_id: UUID) -> None:
        """Mark an event as dispatched."""
        raise NotImplementedError

    @abstractmethod
    async def mark_failed(self, event_id: UUID, error: str) -> None:
        """Record a failed dispatch attempt."""
        raise NotImplementedError


class PostgresOutboxRepository(BaseSQLAlchemyRepository, OutboxRepository):
    """Outbox repository backed by PostgreSQL."""

    _MAX_ATTEMPTS = 5
    _MAX_ERROR_LENGTH = 1024

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @override
    async def append(self, event_type: str, payload: Mapping[str, object]) -> None:
        """See :class:`app.platform.outbox.repository.OutboxRepository.append`."""
        self._session.add(OutboxEventModel(event_type=event_type, payload=dict(payload)))
        await self._session.flush()

    @override
    async def fetch_pending(self, limit: int) -> list[OutboxEvent]:
        """See :class:`app.platform.outbox.repository.OutboxRepository.fetch_pending`."""
        result = await self._session.execute(
            select(OutboxEventModel)
            .where(
                OutboxEventModel.published_at.is_(None),
                OutboxEventModel.attempts < self._MAX_ATTEMPTS,
            )
            .order_by(OutboxEventModel.created_at)
            .limit(limit)
            .with_for_update(skip_locked=True),
        )
        return [
            OutboxEvent(id=model.id, event_type=model.event_type, payload=model.payload)
            for model in result.scalars().all()
        ]

    @override
    async def mark_published(self, event_id: UUID) -> None:
        """See :class:`app.platform.outbox.repository.OutboxRepository.mark_published`."""
        await self._session.execute(
            update(OutboxEventModel)
            .where(OutboxEventModel.id == event_id)
            .values(published_at=datetime.datetime.now(tz=datetime.UTC), last_error=None),
        )

    @override
    async def mark_failed(self, event_id: UUID, error: str) -> None:
        """See :class:`app.platform.outbox.repository.OutboxRepository.mark_failed`."""
        await self._session.execute(
            update(OutboxEventModel)
            .where(OutboxEventModel.id == event_id)
            .values(
                attempts=OutboxEventModel.attempts + 1,
                last_error=error[: self._MAX_ERROR_LENGTH],
            ),
        )


__all__ = ("OutboxEvent", "OutboxRepository", "PostgresOutboxRepository")
