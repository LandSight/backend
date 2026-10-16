"""Interpretation HTTP schemas (Pydantic)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.module.interpretation.domain.value_object import InterpretationStatus


class MetricInfoSchema(BaseModel):
    """One leaf metric of an aspect."""

    key: str = Field(description="Metric key.")
    label: str = Field(default="", description="Human-readable metric name.")
    raw_value: float | None = Field(default=None, description="Raw reading; null when unavailable.")
    normalized_value: float | None = Field(default=None, description="Normalized value in [0, 1].")
    contribution: float | None = Field(default=None, description="Weighted contribution.")
    unit: str = Field(default="", description="Unit of the raw value.")
    role: str = Field(description="Rule-based role (strong/weak/neutral).")
    position: str = Field(
        default="unknown",
        description=(
            "Raw value position relative to the membership function zones "
            "(optimal/partial_low/partial_high/out_low/out_high/unknown)."
        ),
    )
    membership_function: str | None = Field(default=None, description="Applied fuzzy membership function.")
    membership_params: dict[str, float] | None = Field(
        default=None,
        description="Parameters of the membership function, in the metric unit.",
    )


class AspectInterpretationSchema(BaseModel):
    """Explanation of a single aspect."""

    key: str = Field(description="Aspect key.")
    name: str = Field(description="Human-readable aspect name.")
    score: float = Field(description="Aspect score in [0, 1].")
    weight: float = Field(description="Configured aspect weight.")
    contribution: float = Field(description="score * weight.")
    points: float = Field(description="Points the aspect contributed to the total score.")
    max_points: float = Field(description="Points the aspect could contribute at its best.")
    loss: float = Field(description="Points lost from the maximum.")
    loss_share: float = Field(description="Share of the maximum points lost, in [0, 1].")
    explanation: str = Field(description="Human-readable explanation.")
    top_metrics: list[MetricInfoSchema] = Field(
        default_factory=list,
        description="Key metrics selected for the explanation.",
    )
    metrics: list[MetricInfoSchema] = Field(
        default_factory=list,
        description="All leaf metrics of the aspect: strengths, then weaknesses, then metrics without data.",
    )


class ConstraintInterpretationSchema(BaseModel):
    """A restriction zone that barred the scenario or lowered the score."""

    kind: str = Field(description="Restriction zone kind, e.g. power_line_zone.")
    label: str = Field(description="Human-readable name of the zone kind.")
    effect: str = Field(description="prohibit (score set to 0) or penalty (score multiplied by factor).")
    factor: float = Field(ge=0.0, le=1.0, description="Multiplier applied to the score.")
    overlap_share: float = Field(ge=0.0, le=1.0, description="Share of the parcel inside the zone.")
    zone_names: list[str] = Field(default_factory=list, description="Names of the source objects, when known.")
    legal_basis: str = Field(default="", description="Short reference to the rule that defines the zone.")
    score_reduction: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Share of the score the zone takes away on its own (1 - factor).",
    )
    points_lost: float = Field(
        default=0.0,
        ge=0.0,
        description=(
            "Points of the total score attributed to the zone; the points of all zones add up to "
            "constraints_loss. Penalties outweighed by a prohibition get 0."
        ),
    )


class InterpretationResultSchema(BaseModel):
    """Response body of an interpretation report."""

    total_score: float = Field(description="Final score on the configured scale.")
    scale_max: float = Field(description="Maximum score on the configured scale.")
    scenario: str = Field(description="Evaluation profile (e.g. izhs).")
    status: InterpretationStatus = Field(
        default=InterpretationStatus.COMPLETED,
        description="Report generation status: ordered/running/completed/failed.",
    )
    aspects: list[AspectInterpretationSchema] = Field(default_factory=list)
    top_aspects_summary: str = Field(description="Combined explanation of the top aspects.")
    verdict: str | None = Field(
        default=None,
        description=(
            "Suitability verdict code (very_high/high/medium/low/very_low, or prohibited when a "
            "restriction zone bars the scenario); null until generated."
        ),
    )
    verdict_label: str | None = Field(default=None, description="Human-readable verdict.")
    base_score: float | None = Field(
        default=None,
        description="Score of the aspects before the restriction zones; null until generated.",
    )
    constraints_loss: float = Field(
        default=0.0,
        ge=0.0,
        description="Points the restriction zones took away from base_score.",
    )
    constraints_explanation: str = Field(
        default="",
        description="Explanation of the restriction zones; empty when no zone applied.",
    )
    constraints: list[ConstraintInterpretationSchema] = Field(
        default_factory=list,
        description="Restriction zones that barred the scenario or lowered the score, prohibitions first, "
        "then by points_lost.",
    )


__all__ = (
    "AspectInterpretationSchema",
    "ConstraintInterpretationSchema",
    "InterpretationResultSchema",
    "MetricInfoSchema",
)
