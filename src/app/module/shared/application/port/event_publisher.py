"""Event publisher port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Mapping


class EventPublisher(ABC):
    """Port for publishing domain events.

    Implementations are expected to persist events transactionally (outbox), so
    that publishing an event is atomic with the state change that produced it.

    Implementations:
    - :class:`app.platform.outbox.publisher.OutboxEventPublisher`
    """

    @abstractmethod
    async def publish(self, event_type: str, payload: Mapping[str, object]) -> None:
        """Publish an event with a self-contained payload.

        Parameters
        ----------
        event_type : str
            Dotted event type (e.g. ``analysis.analysis_deleted``).
        payload : Mapping[str, object]
            JSON-serializable payload consumed by the event handler.
        """
        raise NotImplementedError


__all__ = ("EventPublisher",)
