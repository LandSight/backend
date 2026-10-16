"""Analysis HTTP schemas (Pydantic)."""

from __future__ import annotations

import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from app.module.analysis.domain.value_object.analysis import AnalysisType
from app.module.analysis.domain.value_object.engine import AnalysisEngine


class StartAnalysisRequest(BaseModel):
    """Request body for starting an analysis."""

    parcel_id: UUID = Field(description="ID of the parcel to analyse.")
    name: str = Field(
        min_length=3,
        max_length=64,
        description="Human-readable name of the analysis.",
    )
    scenario: AnalysisType = Field(
        default=AnalysisType.IZHS,
        description="Evaluation profile. Only 'izhs' (individual housing construction) is available today.",
    )
    engine: AnalysisEngine = Field(
        default=AnalysisEngine.BASELINE,
        description="Scoring engine. Only 'baseline' (fuzzy hierarchical MCDA) is available today.",
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
    scenario: str = Field(description="Evaluation profile (e.g. izhs).")
    engine: str = Field(description="Scoring engine (e.g. baseline).")
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


class ProfileSchema(BaseModel):
    """A single analysis profile in the profile catalogue."""

    key: str = Field(description="Profile identifier (e.g. izhs).")
    name: str = Field(description="Display name of the profile.")
    description: str = Field(description="Description of the profile.")


class ProfilesResponse(BaseModel):
    """Response body listing the available analysis profiles."""

    profiles: list[ProfileSchema] = Field(default_factory=list)


class EngineSchema(BaseModel):
    """A single scoring engine in the engine catalogue."""

    key: str = Field(description="Engine identifier (e.g. baseline).")
    name: str = Field(description="Display name of the engine.")
    description: str = Field(description="Description of the engine.")
    version: str = Field(description="Version of the engine model.")


class EnginesResponse(BaseModel):
    """Response body listing the available scoring engines."""

    engines: list[EngineSchema] = Field(default_factory=list)


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
    label: str = Field(default="", description="Human-readable metric name; empty when not available.")


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
    name: str = Field(default="", description="Human-readable group name; empty when not configured.")


class HierarchicalExtensionSchema(BaseModel):
    """Hierarchical MCDA extension of an evaluation."""

    clusters: list[ClusterScoreSchema] = Field(default_factory=list)


class RuleBasedExtensionSchema(BaseModel):
    """Rule-based extension of an evaluation."""

    base_score: float = Field(description="Score before rules were applied.")
    applied_rules: list[dict[str, Any]] = Field(default_factory=list)


class AppliedConstraintSchema(BaseModel):
    """A restriction zone that changed the score."""

    kind: str = Field(description="Restriction zone kind, e.g. power_line_zone.")
    effect: str = Field(description="prohibit (score set to 0) or penalty (score multiplied by factor).")
    factor: float = Field(ge=0.0, le=1.0, description="Multiplier applied to the score.")
    overlap_share: float = Field(ge=0.0, le=1.0, description="Share of the parcel inside the zone.")
    overlap_area_m2: float = Field(ge=0.0, description="Area of the parcel inside the zone, in square meters.")
    zone_names: list[str] = Field(default_factory=list, description="Names of the source objects, when known.")
    legal_basis: str = Field(default="", description="Short reference to the rule that defines the zone.")


class ConstraintExtensionSchema(BaseModel):
    """Constraint extension of an evaluation."""

    base_score: float = Field(description="Score of the multi-criteria breakdown before the constraints.")
    prohibited: bool = Field(default=False, description="Whether a constraint bars the scenario on the parcel.")
    applied_constraints: list[AppliedConstraintSchema] = Field(default_factory=list)


class EvaluationMetadataSchema(BaseModel):
    """Metadata of an evaluation."""

    evaluated_at: datetime.datetime | None = Field(
        default=None,
        description="When the evaluation was created (UTC).",
    )
    parcel_id: UUID = Field(description="ID of the parcel the evaluation belongs to.")


class AnalysisEvaluationSchema(BaseModel):
    """Response body for a full evaluation.

    The core fields are shared by every engine; ``extensions`` carries
    engine-specific sections keyed by extension name.
    """

    scenario: str = Field(description="Evaluation profile (e.g. izhs).")
    engine: str = Field(description="Scoring engine (e.g. baseline).")
    model_version: str = Field(description="Version of the scoring model.")
    total_score: float = Field(description="Final score on the configured scale.")
    scale_max: float = Field(description="Maximum score on the configured scale.")
    metadata: EvaluationMetadataSchema = Field(description="Evaluation metadata.")
    extensions: dict[
        str,
        HierarchicalExtensionSchema | RuleBasedExtensionSchema | ConstraintExtensionSchema,
    ] = Field(default_factory=dict)


__all__ = (
    "AnalysisEvaluationSchema",
    "AnalysisMetricSchema",
    "AnalysisResponse",
    "AppliedConstraintSchema",
    "ClusterScoreSchema",
    "ConstraintExtensionSchema",
    "EngineSchema",
    "EnginesResponse",
    "EvaluationMetadataSchema",
    "HierarchicalExtensionSchema",
    "MetricContributionSchema",
    "ProfileSchema",
    "ProfilesResponse",
    "RuleBasedExtensionSchema",
    "StartAnalysisRequest",
)
