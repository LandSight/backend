"""Interpretation response DTOs.

These DTOs are the output of the interpretation module: the generated report
assembled from the evaluation and the stored explanations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object import InterpretationStatus, SuitabilityVerdict


if TYPE_CHECKING:
    from app.module.interpretation.domain.value_object import AspectMetric


@dataclass(frozen=True, slots=True)
class AspectInterpretationResponse:
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
    top_metrics: tuple[AspectMetric, ...] = field(default_factory=tuple)
    metrics: tuple[AspectMetric, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class ConstraintInterpretationResponse:
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
class InterpretationResultResponse:
    """Full interpretation report of an analysis evaluation."""

    total_score: float = 0.0
    scale_max: float = 0.0
    scenario: str = ""
    status: InterpretationStatus = InterpretationStatus.COMPLETED
    progress_done: int = 0
    progress_total: int = 0
    aspects: tuple[AspectInterpretationResponse, ...] = field(default_factory=tuple)
    top_aspects_summary: str = ""
    verdict: SuitabilityVerdict | None = None
    base_score: float | None = None
    constraints_loss: float = 0.0
    constraints_explanation: str = ""
    constraints: tuple[ConstraintInterpretationResponse, ...] = field(default_factory=tuple)


__all__ = (
    "AspectInterpretationResponse",
    "ConstraintInterpretationResponse",
    "InterpretationResultResponse",
)
