"""Domain event emitted when an analysis has been scored."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from app.module.analysis.domain.value_object import AnalysisId


if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Self


ANALYSIS_EVALUATED_EVENT = "analysis.analysis_evaluated"


@dataclass(frozen=True, slots=True)
class AnalysisEvaluatedEvent:
    """An analysis whose evaluation has been persisted.

    Consumed to trigger the interpretation report after scoring, outside the
    scoring transaction.

    Attributes
    ----------
    analysis_id : AnalysisId
        ID of the scored analysis.
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

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> Self:
        """Deserialize an ``AnalysisEvaluated`` payload back into the event."""
        analysis_id = payload.get("analysis_id")
        current_user_id = payload.get("current_user_id")
        if analysis_id is None or current_user_id is None:
            message = "AnalysisEvaluated payload must contain 'analysis_id' and 'current_user_id'."
            raise TypeError(message)
        return cls(
            analysis_id=AnalysisId(UUID(str(analysis_id))),
            current_user_id=UUID(str(current_user_id)),
        )


__all__ = ("ANALYSIS_EVALUATED_EVENT", "AnalysisEvaluatedEvent")
