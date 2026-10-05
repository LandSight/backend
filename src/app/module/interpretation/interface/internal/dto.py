"""Internal DTOs for the Interpretation module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object import InterpretationStatus


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.interpretation.domain.value_object import MetricRole


@dataclass(frozen=True, slots=True)
class GetInterpretationInput:
    """Input for retrieving the stored interpretation report of an analysis."""

    analysis_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class GenerateInterpretationInput:
    """Input for generating a fresh interpretation report of an analysis."""

    analysis_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class MetricInfoResult:
    """One metric selected for an aspect explanation."""

    key: str
    label: str
    raw_value: float | None
    normalized_value: float | None
    contribution: float | None
    unit: str
    role: MetricRole


@dataclass(frozen=True, slots=True)
class AspectInterpretationResult:
    """Explanation of a single aspect."""

    key: str
    name: str
    score: float
    weight: float
    contribution: float
    explanation: str
    top_metrics: tuple[MetricInfoResult, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class InterpretationResult:
    """Full interpretation report of an analysis evaluation."""

    total_score: float
    scale_max: float
    scenario: str
    status: InterpretationStatus = InterpretationStatus.COMPLETED
    aspects: tuple[AspectInterpretationResult, ...] = field(default_factory=tuple)
    top_aspects_summary: str = ""


__all__ = (
    "AspectInterpretationResult",
    "GenerateInterpretationInput",
    "GetInterpretationInput",
    "InterpretationResult",
    "MetricInfoResult",
)
