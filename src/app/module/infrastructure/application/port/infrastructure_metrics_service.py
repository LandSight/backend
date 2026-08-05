"""Infrastructure metrics service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.application.dto.response import CategoryMetrics
    from app.module.infrastructure.domain.entity import InfrastructureObject
    from app.module.infrastructure.domain.value_object import Category
    from app.module.shared.interface.internal.geojson import GeoJSONPolygon


class InfrastructureMetricsService(ABC):
    """Port for computing infrastructure metrics from raw objects.

    Computes the metrics for a category given the raw objects found in the
    buffer zone and the parcel geometry. The service is data-source agnostic:
    it only needs the object locations and the parcel boundary.

    Implementations:
    - :class:`app.module.infrastructure.infrastructure.metrics.shapely_infrastructure_metrics_service.ShapelyInfrastructureMetricsService`
    """

    @abstractmethod
    def calculate(
        self,
        objects: list[InfrastructureObject],
        parcel_geometry: GeoJSONPolygon,
        category: Category,
    ) -> CategoryMetrics:
        """Compute metrics for a category from the raw objects.

        Parameters
        ----------
        objects : list[InfrastructureObject]
            Raw objects located within the buffer zone.
        parcel_geometry : GeoJSONPolygon
            Parcel geometry used to measure distances to objects.
        category : Category
            Infrastructure category the metrics are computed for.

        Returns
        -------
        CategoryMetrics
            Computed metrics for the category.
        """
        raise NotImplementedError


__all__ = ("InfrastructureMetricsService",)
