"""Port (abstract base) for the Topography module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.topography.interface.internal.dto import (
        CalculateMetricsInput,
        GetLatestParcelMetricsInput,
        GetMetricsInput,
        ListParcelMetricsInput,
        TopographyMetricsResult,
    )


class TopographyInternalAPI(ABC):
    """Abstract interface for the Topography module's internal API.

    This is the framework-agnostic contract that the HTTP layer
    (``app/interface/http/controller/topography/``) depends on.

    Implementations:
    - :class:`app.module.topography.interface.internal.api.TopographyInternal`
    """

    @abstractmethod
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> TopographyMetricsResult:
        """Calculate topography metrics for a parcel."""
        raise NotImplementedError

    @abstractmethod
    async def get_metrics(self, input_data: GetMetricsInput) -> TopographyMetricsResult:
        """Retrieve a specific topography metrics snapshot by its ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_latest_parcel_metrics(self, input_data: GetLatestParcelMetricsInput) -> TopographyMetricsResult:
        """Retrieve the latest topography metrics for a parcel."""
        raise NotImplementedError

    @abstractmethod
    async def list_parcel_metrics(self, input_data: ListParcelMetricsInput) -> list[TopographyMetricsResult]:
        """List all topography metrics snapshots for a parcel, newest first."""
        raise NotImplementedError


__all__ = ("TopographyInternalAPI",)
