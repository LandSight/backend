"""Random analysis scorer implementation (MVP)."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import AnalysisScorer
from app.module.analysis.domain.value_object import AnalysisScore


if TYPE_CHECKING:
    from app.module.analysis.application.port import MetricsResponse


class RandomAnalysisScorer(AnalysisScorer):
    """MVP scorer that returns a random score in the configured range.

    Accepts the collected metrics responses but ignores them; it is a
    placeholder until a real, rules-based scoring model exists.
    """

    def __init__(self, minimum: float = 0.0, maximum: float = 10.0) -> None:
        self._minimum = minimum
        self._maximum = maximum

    @override
    def score(self, metrics: list[MetricsResponse]) -> AnalysisScore:
        """See :class:`app.module.analysis.application.port.AnalysisScorer.score`."""
        return AnalysisScore(random.uniform(self._minimum, self._maximum))  # noqa: S311


__all__ = ("RandomAnalysisScorer",)
