"""Port (abstract base) for the Infrastructure module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.interface.internal.dto import (
        CalculateMetricsInput,
        CategoryInfoResult,
        GetMetricsInput,
        InfrastructureMetricsResult,
    )


class InfrastructureInternalAPI(ABC):
    """Abstract interface for the Infrastructure module's internal API.

    This is the framework-agnostic contract that the HTTP layer
    (``app/interface/http/controller/infrastructure/``) depends on.

    Implementations:
    - :class:`app.module.infrastructure.interface.internal.api.InfrastructureInternal`
    """

    @abstractmethod
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> InfrastructureMetricsResult:
        """Calculate infrastructure metrics for a parcel."""
        raise NotImplementedError

    @abstractmethod
    async def get_metrics(self, input_data: GetMetricsInput) -> InfrastructureMetricsResult:
        """Retrieve infrastructure metrics for a parcel."""
        raise NotImplementedError

    @abstractmethod
    async def get_available_categories(self) -> list[CategoryInfoResult]:
        """List all available infrastructure categories."""
        raise NotImplementedError


__all__ = ("InfrastructureInternalAPI",)
