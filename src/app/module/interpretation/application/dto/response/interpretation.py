"""Interpretation response DTOs.

These DTOs are the public output of the interpretation module: the result of
turning an evaluation into a human-readable report.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import datetime

    from app.module.interpretation.domain.value_object import MetricRole


@dataclass(frozen=True, slots=True)
class MetricInfoResponse:
    """One metric selected for an aspect explanation."""

    key: str
    label: str
    raw_value: float | None
    normalized_value: float | None
    contribution: float | None
    unit: str
    role: MetricRole


@dataclass(frozen=True, slots=True)
class AspectInterpretationResponse:
    """Explanation of a single aspect."""

    key: str
    name: str
    score: float
    weight: float
    contribution: float
    explanation: str
    top_metrics: tuple[MetricInfoResponse, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class InterpretationMetadataResponse:
    """Metadata of a generated interpretation."""

    evaluated_at: datetime.datetime | None
    parcel_id: str
    llm_model: str
    llm_device: str
    grader_enabled: bool


@dataclass(frozen=True, slots=True)
class InterpretationResultResponse:
    """Full interpretation report of an analysis evaluation."""

    total_score: float
    scale: str
    scenario: str
    metadata: InterpretationMetadataResponse
    aspects: tuple[AspectInterpretationResponse, ...] = field(default_factory=tuple)
    top_aspects_summary: str = ""


__all__ = (
    "AspectInterpretationResponse",
    "InterpretationMetadataResponse",
    "InterpretationResultResponse",
    "MetricInfoResponse",
)
