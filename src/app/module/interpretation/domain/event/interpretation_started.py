"""Domain event emitted when an interpretation report is started for generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID


if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Self


INTERPRETATION_STARTED_EVENT = "interpretation.interpretation_started"


@dataclass(frozen=True, slots=True)
class InterpretationStartedEvent:
    """An interpretation report started for background generation.

    The payload is self-contained so the relay can enqueue the generation task
    after the starting transaction has committed.

    Attributes
    ----------
    analysis_id : UUID
        ID of the analysis the report belongs to.
    current_user_id : UUID
        ID of the user who owns the analysis.
    """

    analysis_id: UUID
    current_user_id: UUID

    def to_payload(self) -> dict[str, object]:
        """Serialize the event into a JSON-compatible payload."""
        return {
            "analysis_id": str(self.analysis_id),
            "current_user_id": str(self.current_user_id),
        }

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> Self:
        """Deserialize an ``InterpretationStarted`` payload back into the event."""
        analysis_id = payload.get("analysis_id")
        current_user_id = payload.get("current_user_id")
        if analysis_id is None or current_user_id is None:
            message = "InterpretationStarted payload must contain 'analysis_id' and 'current_user_id'."
            raise TypeError(message)
        return cls(
            analysis_id=UUID(str(analysis_id)),
            current_user_id=UUID(str(current_user_id)),
        )


__all__ = ("INTERPRETATION_STARTED_EVENT", "InterpretationStartedEvent")
