"""Port (abstract base) for the Topography module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.topography.interface.internal.dto import (
        CalculateMetricsInput,
        GetMetricsInput,
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
        """Retrieve topography metrics for a parcel."""
        raise NotImplementedError


__all__ = ("TopographyInternalAPI",)
