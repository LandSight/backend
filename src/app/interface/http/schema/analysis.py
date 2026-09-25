"""Analysis HTTP schemas (Pydantic)."""

from __future__ import annotations

import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.module.analysis.domain.value_object import AnalysisType


class StartAnalysisRequest(BaseModel):
    """Request body for starting an analysis."""

    parcel_id: UUID = Field(description="ID of the parcel to analyse.")
    name: str = Field(
        min_length=3,
        max_length=64,
        description="Human-readable name of the analysis.",
    )
    analysis_type: AnalysisType = Field(
        default=AnalysisType.IZHS,
        description="Evaluation profile. Only 'izhs' (individual housing construction) is available today.",
    )


class AnalysisResponse(BaseModel):
    """Response body for an analysis."""

    id: UUID = Field(description="Analysis identifier.")
    parcel_id: UUID = Field(description="ID of the parcel being analysed.")
    parcel_name: str | None = Field(
        default=None,
        description="Human-readable name of the parcel; null if it could not be resolved.",
    )
    name: str = Field(description="Human-readable name of the analysis.")
    analysis_type: str = Field(description="Evaluation profile (e.g. izhs).")
    status: str = Field(description="Lifecycle status (pending/running/completed/failed).")
    stage: str = Field(description="Pipeline stage (metrics/scoring).")
    score: float | None = Field(
        default=None,
        description="Final score in [0, 10]; null until the analysis is completed.",
    )
    model_version: str | None = Field(
        default=None,
        description="Version of the scoring model; null until the analysis is completed.",
    )
    status_reason: str | None = Field(
        default=None,
        description="Human-readable status explanation.",
    )
    created_at: datetime.datetime | None = Field(
        default=None,
        description="When the analysis was created (UTC).",
    )
    completed_at: datetime.datetime | None = Field(
        default=None,
        description="When the analysis was completed (UTC); null until completed.",
    )


class AnalysisMetricSchema(BaseModel):
    """Response body for a single analysis metric reference."""

    module: str = Field(description="Metric module the snapshot belongs to (e.g. infrastructure).")
    category: str | None = Field(
        default=None,
        description="Infrastructure category; null for single-metric modules.",
    )
    metrics_id: UUID = Field(description="ID of the persisted metrics snapshot.")


__all__ = (
    "AnalysisMetricSchema",
    "AnalysisResponse",
    "StartAnalysisRequest",
)
