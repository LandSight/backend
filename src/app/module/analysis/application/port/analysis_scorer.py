"""Analysis scorer port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.analysis.domain.value_object import AnalysisScore


class AnalysisScorer(ABC):
    """Port for computing an analysis score.

    Implementations:
    - :class:`app.module.analysis.infrastructure.scoring.random_analysis_scorer.RandomAnalysisScorer`
    """

    @abstractmethod
    def score(self) -> AnalysisScore:
        """Compute the analysis score.

        Returns
        -------
        AnalysisScore
            The computed score in [0, 10].
        """
        raise NotImplementedError


__all__ = ("AnalysisScorer",)
