"""Metrics repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.domain.entity import (
        HospitalMetrics,
        InfrastructureMetrics,
        SchoolMetrics,
        ShopMetrics,
        TransitStopMetrics,
        WaterBodyMetrics,
    )
    from app.module.infrastructure.domain.value_object import Category, ParcelId


class MetricsRepository(ABC):
    """Port for infrastructure metrics persistence.

    Each category has its own save method dispatching to its dedicated table
    (e.g. ``parcel_school_metrics``).

    Implementations:
    - :class:`app.module.infrastructure.infrastructure.repository.postgres_metrics_repository.PostgresMetricsRepository`
    """

    @abstractmethod
    async def save_schools(self, metrics: SchoolMetrics) -> None:
        """Persist school metrics."""
        raise NotImplementedError

    @abstractmethod
    async def save_hospitals(self, metrics: HospitalMetrics) -> None:
        """Persist hospital metrics."""
        raise NotImplementedError

    @abstractmethod
    async def save_shops(self, metrics: ShopMetrics) -> None:
        """Persist shop metrics."""
        raise NotImplementedError

    @abstractmethod
    async def save_transit_stops(self, metrics: TransitStopMetrics) -> None:
        """Persist transit stop metrics."""
        raise NotImplementedError

    @abstractmethod
    async def save_water_bodies(self, metrics: WaterBodyMetrics) -> None:
        """Persist water body metrics."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_parcel_id_and_category(
        self,
        parcel_id: ParcelId,
        category: Category,
    ) -> InfrastructureMetrics | None:
        """Retrieve infrastructure metrics by parcel ID and category.

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.
        category : Category
            Infrastructure category.

        Returns
        -------
        InfrastructureMetrics | None
            The metrics if found, ``None`` otherwise.
        """
        raise NotImplementedError


__all__ = ("MetricsRepository",)
