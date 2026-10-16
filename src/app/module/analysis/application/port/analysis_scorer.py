"""Analysis scorer port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Sequence
    from uuid import UUID

    from app.module.analysis.application.port.metrics_service import MetricsResponse
    from app.module.analysis.domain.entity import AnalysisEvaluation
    from app.module.analysis.domain.value_object import AnalysisEngine, AnalysisType, RestrictionHit


class AnalysisScorer(ABC):
    """Port for evaluating collected metrics into a universal result.

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
        restrictions: Sequence[RestrictionHit] = (),
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
        restrictions : Sequence[RestrictionHit]
            Restrictions on the parcel; the profile's constraint
            policy decides which bar the scenario and which lower the score.

        Returns
        -------
        AnalysisEvaluation
            The full evaluation aggregate, including the total score in ``[0, 10]``
            after the constraints and the score before them.
        """
        raise NotImplementedError


__all__ = ("AnalysisScorer",)
