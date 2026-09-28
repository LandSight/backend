"""Domain event emitted when an analysis is queued for processing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from app.module.analysis.domain.value_object import AnalysisId


if TYPE_CHECKING:
    from collections.abc import Mapping


ANALYSIS_QUEUED_EVENT = "analysis.analysis_queued"


@dataclass(frozen=True, slots=True)
class AnalysisQueuedEvent:
    """An analysis queued for background processing.

    The payload is self-contained so the relay can enqueue the processing task
    after the creating transaction has committed.

    Attributes
    ----------
    analysis_id : AnalysisId
        ID of the analysis to process.
    current_user_id : UUID
        ID of the user who started the analysis.
    """

    analysis_id: AnalysisId
    current_user_id: UUID

    def to_payload(self) -> dict[str, object]:
        """Serialize the event into a JSON-compatible payload."""
        return {
            "analysis_id": str(self.analysis_id.unwrap()),
            "current_user_id": str(self.current_user_id),
        }


def analysis_queued_from_payload(payload: Mapping[str, object]) -> tuple[AnalysisId, UUID]:
    """Deserialize an ``AnalysisQueued`` payload.

    Parameters
    ----------
    payload : Mapping[str, object]
        Event payload produced by :meth:`AnalysisQueuedEvent.to_payload`.

    Returns
    -------
    tuple[AnalysisId, UUID]
        The analysis ID and the user ID that started it.

    Raises
    ------
    TypeError
        If the payload is malformed.
    """
    analysis_id = payload.get("analysis_id")
    current_user_id = payload.get("current_user_id")
    if analysis_id is None or current_user_id is None:
        message = "AnalysisQueued payload must contain 'analysis_id' and 'current_user_id'."
        raise TypeError(message)
    return AnalysisId(UUID(str(analysis_id))), UUID(str(current_user_id))


__all__ = ("ANALYSIS_QUEUED_EVENT", "AnalysisQueuedEvent", "analysis_queued_from_payload")
