"""Internal DTOs for the Interpretation module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object import InterpretationStatus, SuitabilityVerdict, ValuePosition


if TYPE_CHECKING:
    from collections.abc import Mapping
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
class CancelInterpretationInput:
    """Input for cancelling the generation of an interpretation report."""

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
    position: ValuePosition = ValuePosition.UNKNOWN
    membership_function: str | None = None
    membership_params: Mapping[str, float] | None = None


@dataclass(frozen=True, slots=True)
class AspectInterpretationResult:
    """Explanation of a single aspect."""

    key: str
    name: str
    score: float
    weight: float
    contribution: float
    points: float
    max_points: float
    loss: float
    loss_share: float
    explanation: str
    top_metrics: tuple[MetricInfoResult, ...] = field(default_factory=tuple)
    metrics: tuple[MetricInfoResult, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class ConstraintInterpretationResult:
    """A restriction zone that barred the scenario or lowered the score."""

    kind: str
    label: str
    effect: str
    factor: float
    overlap_share: float
    zone_names: tuple[str, ...] = field(default_factory=tuple)
    legal_basis: str = ""
    score_reduction: float = 0.0
    points_lost: float = 0.0


@dataclass(frozen=True, slots=True)
class InterpretationResult:
    """Full interpretation report of an analysis evaluation."""

    total_score: float
    scale_max: float
    scenario: str
    status: InterpretationStatus = InterpretationStatus.COMPLETED
    progress_done: int = 0
    progress_total: int = 0
    aspects: tuple[AspectInterpretationResult, ...] = field(default_factory=tuple)
    top_aspects_summary: str = ""
    verdict: SuitabilityVerdict | None = None
    base_score: float | None = None
    constraints_loss: float = 0.0
    constraints_explanation: str = ""
    constraints: tuple[ConstraintInterpretationResult, ...] = field(default_factory=tuple)


__all__ = (
    "AspectInterpretationResult",
    "CancelInterpretationInput",
    "ConstraintInterpretationResult",
    "GenerateInterpretationInput",
    "GetInterpretationInput",
    "InterpretationResult",
    "MetricInfoResult",
)
