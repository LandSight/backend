"""Metrics remover port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.analysis.domain.value_object import AnalysisMetricRef


class MetricsRemover(ABC):
    """Port for deleting metric snapshots referenced by an analysis.

    Implementations:
    - :class:`app.module.analysis.infrastructure.remover.metrics_remover.MetricsRemoverImpl`
    """

    @abstractmethod
    async def delete(self, refs: list[AnalysisMetricRef]) -> None:
        """Delete the metric snapshots behind the given references.

        Parameters
        ----------
        refs : list[AnalysisMetricRef]
            Metric references to delete.
        """
        raise NotImplementedError


__all__ = ("MetricsRemover",)
