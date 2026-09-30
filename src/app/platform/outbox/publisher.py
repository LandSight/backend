"""Outbox-backed event publisher."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.shared.application.port import EventPublisher


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.platform.outbox.repository import OutboxRepository


class OutboxEventPublisher(EventPublisher):
    """Persist events to the transactional outbox.

    The event is written through the repository bound to the caller's session,
    so it commits atomically with the surrounding state change.
    """

    def __init__(self, repository: OutboxRepository) -> None:
        self._repository = repository

    @override
    async def publish(self, event_type: str, payload: Mapping[str, object]) -> None:
        """See :class:`app.module.shared.application.port.EventPublisher.publish`."""
        await self._repository.append(event_type, payload)


__all__ = ("OutboxEventPublisher",)
