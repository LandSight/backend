"""Port (abstract base) for the Climate module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.climate.interface.internal.dto import (
        CalculateMetricsInput,
        DeleteMetricsInput,
        GetMetricsInput,
        GetParcelMetricsInput,
    )
    from app.module.shared.interface.internal import MetricsResponse


class ClimateInternalAPI(ABC):
    """Abstract interface for the Climate module's internal API.

    Metrics are returned as a neutral ``list[MetricValue]`` so that internal and
    HTTP consumers receive the same generic shape.

    Implementations:
    - :class:`app.module.climate.interface.internal.api.ClimateInternal`
    """

    @abstractmethod
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> MetricsResponse:
        """Calculate climate metrics for a parcel and return a neutral response."""
        raise NotImplementedError

    @abstractmethod
    async def get_metrics(self, input_data: GetMetricsInput) -> MetricsResponse:
        """Retrieve a specific climate metrics snapshot as a neutral response."""
        raise NotImplementedError

    @abstractmethod
    async def get_parcel_metrics(self, input_data: GetParcelMetricsInput) -> MetricsResponse:
        """Retrieve the current climate metrics for a parcel as a neutral response."""
        raise NotImplementedError

    @abstractmethod
    async def delete_metrics(self, input_data: DeleteMetricsInput) -> None:
        """Delete climate metrics snapshots by their IDs."""
        raise NotImplementedError


__all__ = ("ClimateInternalAPI",)
