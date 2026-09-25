"""Analysis response DTO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import datetime
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class AnalysisResponse:
    """Response DTO for an analysis.

    Attributes
    ----------
    id : UUID
        Analysis identifier.
    parcel_id : UUID
        ID of the parcel being analysed.
    parcel_name : str | None
        Human-readable name of the parcel; ``None`` if it could not be resolved.
    name : str
        Human-readable name of the analysis.
    analysis_type : str
        Evaluation profile the analysis was run with.
    status : str
        Lifecycle status (pending/running/completed/failed).
    stage : str
        Pipeline stage (metrics/scoring).
    score : float | None
        Final score in [0, 10]; ``None`` until completed.
    model_version : str | None
        Version of the scoring model; ``None`` until completed.
    status_reason : str | None
        Human-readable status explanation.
    created_at : datetime.datetime | None
        When the analysis was created (UTC).
    completed_at : datetime.datetime | None
        When the analysis was completed (UTC); ``None`` until completed.
    """

    id: UUID
    parcel_id: UUID
    parcel_name: str | None
    name: str
    analysis_type: str
    status: str
    stage: str
    score: float | None
    model_version: str | None
    status_reason: str | None
    created_at: datetime.datetime | None
    completed_at: datetime.datetime | None


__all__ = ("AnalysisResponse",)
