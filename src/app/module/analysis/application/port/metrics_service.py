"""Metrics service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.module.shared.interface.internal import MetricsResponse


if TYPE_CHECKING:
    from collections.abc import Mapping
    from uuid import UUID

    from app.module.analysis.domain.value_object import AnalysisMetricRef


class MetricsService(ABC):
    """Gateway to the metric modules' internal APIs.

    A single client for everything the analysis pipeline needs from the metric
    modules: calculating snapshots, reading their values and deleting them.

    Implementations:
    - :class:`app.module.analysis.infrastructure.gateway.metrics_service.MetricsServiceImpl`
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
        buffers: Mapping[str, int],
    ) -> list[AnalysisMetricRef]:
        """Calculate and persist infrastructure metrics for the configured categories."""
        raise NotImplementedError

    @abstractmethod
    async def get_metrics(
        self,
        parcel_id: UUID,
        refs: list[AnalysisMetricRef],
        user_id: UUID,
    ) -> list[MetricsResponse]:
        """Read the neutral metrics responses behind the given references."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, refs: list[AnalysisMetricRef]) -> None:
        """Delete the metric snapshots behind the given references."""
        raise NotImplementedError


__all__ = ("MetricsResponse", "MetricsService")
