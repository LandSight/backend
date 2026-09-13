"""Port (abstract base) for the Infrastructure module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.interface.internal.dto import (
        CalculateMetricsInput,
        CategoryInfoResult,
        GetMetricsByIdsInput,
        GetMetricsInput,
    )
    from app.module.shared.interface.internal import MetricsResponse


class InfrastructureInternalAPI(ABC):
    """Abstract interface for the Infrastructure module's internal API.

    Metrics are returned as a neutral ``list[MetricValue]`` so that internal and
    HTTP consumers receive the same generic shape.

    Implementations:
    - :class:`app.module.infrastructure.interface.internal.api.InfrastructureInternal`
    """

    @abstractmethod
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> list[MetricsResponse]:
        """Calculate infrastructure metrics for a parcel and return neutral values."""
        raise NotImplementedError

    @abstractmethod
    async def get_metrics(self, input_data: GetMetricsInput) -> list[MetricsResponse]:
        """Retrieve infrastructure metrics for a parcel as neutral values."""
        raise NotImplementedError

    @abstractmethod
    async def get_metrics_by_ids(self, input_data: GetMetricsByIdsInput) -> list[MetricsResponse]:
        """Retrieve specific infrastructure metrics records as neutral values."""
        raise NotImplementedError

    @abstractmethod
    async def get_available_categories(self) -> list[CategoryInfoResult]:
        """List all available infrastructure categories."""
        raise NotImplementedError


__all__ = ("InfrastructureInternalAPI",)
