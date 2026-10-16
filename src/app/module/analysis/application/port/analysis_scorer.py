"""Analysis scorer port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.application.port.metrics_service import MetricsResponse
    from app.module.analysis.domain.entity import AnalysisEvaluation
    from app.module.analysis.domain.value_object.analysis import AnalysisType
    from app.module.analysis.domain.value_object.engine import AnalysisEngine


class AnalysisScorer(ABC):
    """Port for evaluating collected metrics into a universal result.

    A scorer only rates the metrics; restrictions are applied to its score
    afterwards by the :class:`ConstraintEvaluator`.

    Implementations:
    - :class:`app.module.analysis.infrastructure.scorer.hmcda.hmcda_analysis_scorer.HmcdaAnalysisScorer`
    """

    @abstractmethod
    def evaluate(
        self,
        analysis_id: UUID,
        metrics: list[MetricsResponse],
        analysis_type: AnalysisType,
        engine: AnalysisEngine,
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
        engine : AnalysisEngine
            Scoring engine to evaluate with. Implementations must reject engines
            they do not support.

        Returns
        -------
        AnalysisEvaluation
            The evaluation of the metrics, with the total score in ``[0, 10]``;
            constraints are applied afterwards and separately.
        """
        raise NotImplementedError


__all__ = ("AnalysisScorer",)
