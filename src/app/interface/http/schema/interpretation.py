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
        description="Suitability verdict code (very_high/high/medium/low/very_low); null until generated.",
    )
    verdict_label: str | None = Field(default=None, description="Human-readable verdict.")


__all__ = (
    "AspectInterpretationSchema",
    "InterpretationResultSchema",
    "MetricInfoSchema",
)
