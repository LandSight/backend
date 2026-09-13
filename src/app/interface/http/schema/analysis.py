"""Analysis HTTP schemas (Pydantic)."""

from __future__ import annotations

import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class StartAnalysisRequest(BaseModel):
    """Request body for starting an analysis."""

    parcel_id: UUID = Field(description="ID of the parcel to analyse.")
    name: str = Field(
        min_length=3,
        max_length=64,
        description="Human-readable name of the analysis.",
    )


class AnalysisResponse(BaseModel):
    """Response body for an analysis."""

    id: UUID = Field(description="Analysis identifier.")
    parcel_id: UUID = Field(description="ID of the parcel being analysed.")
    name: str = Field(description="Human-readable name of the analysis.")
    status: str = Field(description="Lifecycle status (pending/running/completed/failed).")
    score: float | None = Field(
        default=None,
        description="Final score in [0, 10]; null until the analysis is completed.",
    )
    status_reason: str | None = Field(
        default=None,
        description="Human-readable status explanation.",
    )
    created_at: datetime.datetime | None = Field(
        default=None,
        description="When the analysis was created (UTC).",
    )


__all__ = (
    "AnalysisResponse",
    "StartAnalysisRequest",
)
