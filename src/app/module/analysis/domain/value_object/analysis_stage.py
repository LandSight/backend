"""Analysis processing stage value object."""

from __future__ import annotations

from enum import StrEnum


class AnalysisStage(StrEnum):
    """Current stage of the analysis pipeline.

    ``METRICS``
        Calculating and persisting metric snapshots.
    ``SCORING``
        Metrics are ready; computing the final score.
    """

    METRICS = "metrics"
    SCORING = "scoring"


__all__ = ("AnalysisStage",)
