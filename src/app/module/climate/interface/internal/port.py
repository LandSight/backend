"""Port (abstract base) for the Climate module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.climate.interface.internal.dto import (
        CalculateMetricsInput,
        ClimateMetricsResult,
        GetMetricsInput,
        GetParcelMetricsInput,
    )


class ClimateInternalAPI(ABC):
    """Abstract interface for the Climate module's internal API.

    This is the framework-agnostic contract that the HTTP layer
    (``app/interface/http/controller/climate/``) depends on.

    Implementations:
    - :class:`app.module.climate.interface.internal.api.ClimateInternal`
    """

    @abstractmethod
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> ClimateMetricsResult:
        """Calculate climate metrics for a parcel."""
        raise NotImplementedError

    @abstractmethod
    async def get_metrics(self, input_data: GetMetricsInput) -> ClimateMetricsResult:
        """Retrieve a specific climate metrics snapshot by its ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_parcel_metrics(self, input_data: GetParcelMetricsInput) -> ClimateMetricsResult:
        """Retrieve the current climate metrics for a parcel."""
        raise NotImplementedError


__all__ = ("ClimateInternalAPI",)
