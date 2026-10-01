"""Evaluation breakdown builder port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.analysis.application.dto.response import AnalysisEvaluationResponse
    from app.module.interpretation.domain.value_object import EvaluationBreakdown


class EvaluationBreakdownBuilder(ABC):
    """Maps an analysis evaluation response to the interpretation domain model."""

    @abstractmethod
    def build(self, response: AnalysisEvaluationResponse) -> EvaluationBreakdown:
        """Build the flat domain breakdown of an evaluation response."""
        raise NotImplementedError


__all__ = ("EvaluationBreakdownBuilder",)
