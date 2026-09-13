"""Analysis scorer port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.analysis.application.port.metrics_reader import MetricsResponse
    from app.module.analysis.domain.value_object import AnalysisScore


class AnalysisScorer(ABC):
    """Port for computing an analysis score from collected metrics responses.

    Implementations:
    - :class:`app.module.analysis.infrastructure.scoring.random_analysis_scorer.RandomAnalysisScorer`
    """

    @abstractmethod
    def score(self, metrics: list[MetricsResponse]) -> AnalysisScore:
        """Compute the analysis score.

        Parameters
        ----------
        metrics : list[MetricsResponse]
            Neutral metrics responses read for the analysis.

        Returns
        -------
        AnalysisScore
            The computed score in [0, 10].
        """
        raise NotImplementedError


__all__ = ("AnalysisScorer",)
