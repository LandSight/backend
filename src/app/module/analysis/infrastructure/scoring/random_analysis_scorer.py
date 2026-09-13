"""Random analysis scorer implementation (MVP)."""

from __future__ import annotations

import random
from typing import override

from app.module.analysis.application.port import AnalysisScorer
from app.module.analysis.domain.value_object import AnalysisScore


class RandomAnalysisScorer(AnalysisScorer):
    """MVP scorer that returns a random score in the configured range.

    This is a placeholder until a real metrics-based scoring model exists.
    """

    def __init__(self, minimum: float = 0.0, maximum: float = 10.0) -> None:
        self._minimum = minimum
        self._maximum = maximum

    @override
    def score(self) -> AnalysisScore:
        """See :class:`app.module.analysis.application.port.AnalysisScorer.score`."""
        return AnalysisScore(random.uniform(self._minimum, self._maximum))  # noqa: S311


__all__ = ("RandomAnalysisScorer",)
