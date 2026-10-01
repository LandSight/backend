"""Interpretation response DTOs.

These DTOs are the output of the interpretation module: the generated report
assembled from the evaluation and the stored explanations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


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
    explanation: str
    top_metrics: tuple[AspectMetric, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class InterpretationResultResponse:
    """Full interpretation report of an analysis evaluation."""

    total_score: float
    scale: str
    scenario: str
    aspects: tuple[AspectInterpretationResponse, ...] = field(default_factory=tuple)
    top_aspects_summary: str = ""


__all__ = (
    "AspectInterpretationResponse",
    "InterpretationResultResponse",
)
