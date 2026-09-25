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


class MetricContributionSchema(BaseModel):
    """Response body for one metric contribution in an evaluation."""

    key: str = Field(description="Metric key.")
    raw_value: float | None = Field(default=None, description="Raw reading; null when unavailable.")
    normalized_value: float | None = Field(default=None, description="Normalized value in [0, 1].")
    weight: float = Field(description="Configured weight among siblings.")
    contribution: float | None = Field(default=None, description="Weighted contribution.")
    unit: str = Field(description="Unit of the raw value.")
    data_available: bool = Field(description="Whether a usable reading was available.")
    membership_function: str | None = Field(default=None, description="Applied membership function.")
    membership_params: dict[str, float] | None = Field(
        default=None,
        description="Parameters of the applied membership function.",
    )


class ClusterScoreSchema(BaseModel):
    """Response body for a group score.

    The same shape represents a top-level cluster and a nested subcluster.
    """

    key: str = Field(description="Group key.")
    score: float = Field(description="Aggregated score in [0, 1].")
    weight: float = Field(description="Configured weight within the parent.")
    contribution: float = Field(description="score * weight.")
    subclusters: list[ClusterScoreSchema] = Field(default_factory=list)
    metrics: list[MetricContributionSchema] = Field(default_factory=list)


class AnalysisEvaluationSchema(BaseModel):
    """Response body for a full evaluation tree."""

    analysis_id: str = Field(description="Analysis identifier.")
    analysis_type: str = Field(description="Evaluation profile (e.g. izhs).")
    model_version: str = Field(description="Version of the scoring model.")
    total_score: float = Field(description="Final score on the 0-10 scale.")
    scale: str = Field(description="Score scale.")
    clusters: list[ClusterScoreSchema] = Field(default_factory=list)


__all__ = (
    "AnalysisEvaluationSchema",
    "AnalysisMetricSchema",
    "AnalysisResponse",
    "ClusterScoreSchema",
    "MetricContributionSchema",
    "StartAnalysisRequest",
)
