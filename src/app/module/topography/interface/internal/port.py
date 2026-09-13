"""Port (abstract base) for the Topography module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.shared.interface.internal import MetricsResponse
    from app.module.topography.interface.internal.dto import (
        CalculateMetricsInput,
        GetMetricsInput,
        GetParcelMetricsInput,
    )


class TopographyInternalAPI(ABC):
    """Abstract interface for the Topography module's internal API.

    Metrics are returned as a neutral ``list[MetricValue]`` so that internal and
    HTTP consumers receive the same generic shape.

    Implementations:
    - :class:`app.module.topography.interface.internal.api.TopographyInternal`
    """

    @abstractmethod
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> MetricsResponse:
        """Calculate topography metrics for a parcel and return a neutral response."""
        raise NotImplementedError

    @abstractmethod
    async def get_metrics(self, input_data: GetMetricsInput) -> MetricsResponse:
        """Retrieve a specific topography metrics snapshot as a neutral response."""
        raise NotImplementedError

    @abstractmethod
    async def get_parcel_metrics(self, input_data: GetParcelMetricsInput) -> MetricsResponse:
        """Retrieve the current topography metrics for a parcel as a neutral response."""
        raise NotImplementedError


__all__ = ("TopographyInternalAPI",)
