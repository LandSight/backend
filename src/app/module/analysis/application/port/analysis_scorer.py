"""Analysis scorer port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.application.port.metrics_reader import MetricsResponse
    from app.module.analysis.domain.entity import AnalysisEvaluation
    from app.module.analysis.domain.value_object import AnalysisType


class AnalysisScorer(ABC):
    """Port for evaluating collected metrics into a hierarchical MCDA result.

    Implementations:
    - :class:`app.module.analysis.infrastructure.scorer.hmcda_analysis_scorer.HmcdaAnalysisScorer`
    """

    @abstractmethod
    def evaluate(
        self,
        analysis_id: UUID,
        metrics: list[MetricsResponse],
        analysis_type: AnalysisType,
    ) -> AnalysisEvaluation:
        """Evaluate the collected metrics.

        Parameters
        ----------
        analysis_id : UUID
            ID of the analysis being scored.
        metrics : list[MetricsResponse]
            Neutral metrics responses read for the analysis.
        analysis_type : AnalysisType
            Evaluation profile to score with.

        Returns
        -------
        AnalysisEvaluation
            The full evaluation aggregate, including the total score in ``[0, 10]``.
        """
        raise NotImplementedError


__all__ = ("AnalysisScorer",)
