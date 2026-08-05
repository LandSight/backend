"""Infrastructure metrics service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.application.dto.response import CategoryMetricsResponse
    from app.module.infrastructure.domain.entity import InfrastructureObject
    from app.module.shared.domain.value_object import Polygon


class InfrastructureMetricsService(ABC):
    """Port for computing infrastructure metrics from raw objects.

    Each category has its own method so that categories can compute different
    metrics and validate their own invariants. The service is data-source
    agnostic: it only needs the object locations and the parcel geometry.

    Implementations:
    - :class:`app.module.infrastructure.infrastructure.metrics.shapely_infrastructure_metrics_service.ShapelyInfrastructureMetricsService`
    """

    @abstractmethod
    def calculate_schools(
        self,
        objects: list[InfrastructureObject],
        parcel_geometry: Polygon,
    ) -> CategoryMetricsResponse:
        """Compute metrics for the ``schools`` category."""
        raise NotImplementedError

    @abstractmethod
    def calculate_hospitals(
        self,
        objects: list[InfrastructureObject],
        parcel_geometry: Polygon,
    ) -> CategoryMetricsResponse:
        """Compute metrics for the ``hospitals`` category."""
        raise NotImplementedError

    @abstractmethod
    def calculate_shops(
        self,
        objects: list[InfrastructureObject],
        parcel_geometry: Polygon,
    ) -> CategoryMetricsResponse:
        """Compute metrics for the ``shops`` category."""
        raise NotImplementedError

    @abstractmethod
    def calculate_transit_stops(
        self,
        objects: list[InfrastructureObject],
        parcel_geometry: Polygon,
    ) -> CategoryMetricsResponse:
        """Compute metrics for the ``transit_stops`` category."""
        raise NotImplementedError


__all__ = ("InfrastructureMetricsService",)
