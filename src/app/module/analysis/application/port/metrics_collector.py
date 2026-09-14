"""Metrics collector port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.domain.value_object import AnalysisMetricRef


class MetricsCollector(ABC):
    """Port for calculating the metrics required by an analysis.

    Each method calculates and persists the module's metrics snapshots, then
    returns the references to record for the analysis.

    Implementations:
    - :class:`app.module.analysis.infrastructure.collector.metrics_collector.MetricsCollectorImpl`
    """

    @abstractmethod
    async def collect_topography(self, parcel_id: UUID, user_id: UUID) -> AnalysisMetricRef:
        """Calculate and persist topography metrics for a parcel."""
        raise NotImplementedError

    @abstractmethod
    async def collect_climate(self, parcel_id: UUID, user_id: UUID) -> AnalysisMetricRef:
        """Calculate and persist climate metrics for a parcel."""
        raise NotImplementedError

    @abstractmethod
    async def collect_infrastructure(
        self,
        parcel_id: UUID,
        user_id: UUID,
        buffers: dict[str, int],
    ) -> list[AnalysisMetricRef]:
        """Calculate and persist infrastructure metrics for the configured categories."""
        raise NotImplementedError


__all__ = ("MetricsCollector",)
