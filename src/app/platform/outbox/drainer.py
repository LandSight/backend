"""Outbox relay that dispatches pending events to their handlers."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from typing import TYPE_CHECKING

from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.platform.outbox.repository import OutboxRepository


EventHandler = Callable[[Mapping[str, object]], Awaitable[None]]


class OutboxDrainer:
    """Dispatch pending outbox events, isolating handler failures per event.

    The drainer does not commit: the caller owns the transaction so that locking
    (``SKIP LOCKED``) and the dispatch result are committed together.
    """

    def __init__(
        self,
        repository: OutboxRepository,
        handlers: Mapping[str, EventHandler],
        limit: int = 100,
    ) -> None:
        self._repository = repository
        self._handlers = handlers
        self._limit = limit
        self._logger = get_logger("app.platform.outbox.drainer")

    async def drain(self) -> int:
        """Dispatch pending events and return how many were processed."""
        events = await self._repository.fetch_pending(self._limit)
        for event in events:
            handler = self._handlers.get(event.event_type)
            if handler is None:
                await self._repository.mark_failed(
                    event.id,
                    f"No handler registered for event '{event.event_type}'.",
                )
                continue
            try:
                await handler(event.payload)
            except Exception as exc:
                self._logger.warning(
                    "Outbox event dispatch failed: event_id=%s type=%s error=%s",
                    event.id,
                    event.event_type,
                    exc,
                )
                await self._repository.mark_failed(event.id, str(exc))
            else:
                await self._repository.mark_published(event.id)
        return len(events)


__all__ = ("EventHandler", "OutboxDrainer")
