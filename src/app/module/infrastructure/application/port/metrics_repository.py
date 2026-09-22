"""Metrics repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.domain.entity import (
        EcologyMetrics,
        FacilityMetrics,
        GeographicPositionMetrics,
        RoadAccessibilityMetrics,
        UtilityMetrics,
    )
    from app.module.infrastructure.domain.value_object import (
        Buffer,
        Category,
        InfrastructureMetricsId,
        ParcelId,
    )


class MetricsRepository(ABC):
    """Port for infrastructure metrics persistence.

    Metrics are grouped into families that share the same storage table. Methods
    are per family and take the category so the correct type row is loaded.

    Implementations:
    - :class:`app.module.infrastructure.infrastructure.repository.postgres_metrics_repository.PostgresMetricsRepository`
    """

    @abstractmethod
    async def delete(self, refs: list[tuple[Category, InfrastructureMetricsId]]) -> None:
        """Delete metrics snapshots for the given ``(category, id)`` references."""
        raise NotImplementedError

    # ----- Facility -----

    @abstractmethod
    async def save_facility(self, metrics: FacilityMetrics) -> None:
        """Persist facility metrics."""
        raise NotImplementedError

    @abstractmethod
    async def get_facility(
        self,
        parcel_id: ParcelId,
        category: Category,
        buffer: Buffer | None = None,
    ) -> FacilityMetrics | None:
        """Retrieve facility metrics for a parcel and category."""
        raise NotImplementedError

    @abstractmethod
    async def get_facility_by_id(self, metrics_id: InfrastructureMetricsId) -> FacilityMetrics | None:
        """Retrieve a specific facility metrics record by its ID."""
        raise NotImplementedError

    # ----- Ecology -----

    @abstractmethod
    async def save_ecology(self, metrics: EcologyMetrics) -> None:
        """Persist ecology metrics."""
        raise NotImplementedError

    @abstractmethod
    async def get_ecology(
        self,
        parcel_id: ParcelId,
        category: Category,
        buffer: Buffer | None = None,
    ) -> EcologyMetrics | None:
        """Retrieve ecology metrics for a parcel and category."""
        raise NotImplementedError

    @abstractmethod
    async def get_ecology_by_id(self, metrics_id: InfrastructureMetricsId) -> EcologyMetrics | None:
        """Retrieve a specific ecology metrics record by its ID."""
        raise NotImplementedError

    # ----- Utility -----

    @abstractmethod
    async def save_utility(self, metrics: UtilityMetrics) -> None:
        """Persist utility metrics."""
        raise NotImplementedError

    @abstractmethod
    async def get_utility(
        self,
        parcel_id: ParcelId,
        category: Category,
        buffer: Buffer | None = None,
    ) -> UtilityMetrics | None:
        """Retrieve utility metrics for a parcel and category."""
        raise NotImplementedError

    @abstractmethod
    async def get_utility_by_id(self, metrics_id: InfrastructureMetricsId) -> UtilityMetrics | None:
        """Retrieve a specific utility metrics record by its ID."""
        raise NotImplementedError

    # ----- Road accessibility -----

    @abstractmethod
    async def save_road_accessibility(self, metrics: RoadAccessibilityMetrics) -> None:
        """Persist road accessibility metrics."""
        raise NotImplementedError

    @abstractmethod
    async def get_road_accessibility(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> RoadAccessibilityMetrics | None:
        """Retrieve road accessibility metrics for a parcel."""
        raise NotImplementedError

    @abstractmethod
    async def get_road_accessibility_by_id(
        self,
        metrics_id: InfrastructureMetricsId,
    ) -> RoadAccessibilityMetrics | None:
        """Retrieve a specific road accessibility metrics record by its ID."""
        raise NotImplementedError

    # ----- Geographic position -----

    @abstractmethod
    async def save_geographic_position(self, metrics: GeographicPositionMetrics) -> None:
        """Persist geographic position metrics."""
        raise NotImplementedError

    @abstractmethod
    async def get_geographic_position(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> GeographicPositionMetrics | None:
        """Retrieve geographic position metrics for a parcel."""
        raise NotImplementedError

    @abstractmethod
    async def get_geographic_position_by_id(
        self,
        metrics_id: InfrastructureMetricsId,
    ) -> GeographicPositionMetrics | None:
        """Retrieve a specific geographic position metrics record by its ID."""
        raise NotImplementedError


__all__ = ("MetricsRepository",)
