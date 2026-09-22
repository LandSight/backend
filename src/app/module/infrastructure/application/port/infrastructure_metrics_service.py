"""Infrastructure metrics service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Iterable

    from app.module.infrastructure.domain.entity import InfrastructureObject
    from app.module.infrastructure.domain.value_object import (
        BufferZone,
        Count,
        CoverageRatio,
        Density,
        Distance,
    )
    from app.module.shared.domain.value_object import Polygon


class InfrastructureMetricsService(ABC):
    """Port for computing individual infrastructure metrics.

    Each method performs a single action and returns a single value object.
    The use case assembles the metrics entity and response from these values.
    """

    @abstractmethod
    def count_objects(self, objects: list[InfrastructureObject]) -> Count:
        """Count the number of objects."""
        raise NotImplementedError

    @abstractmethod
    def count_components(self, objects: list[InfrastructureObject]) -> Count:
        """Count the distinct connected objects after merging touching geometries.

        Fragmented OSM mapping of a single object (e.g. a lake split into several
        ways) yields one component instead of many, so the count reflects real
        objects rather than map geometry pieces.
        """
        raise NotImplementedError

    @abstractmethod
    def min_distance(
        self,
        objects: list[InfrastructureObject],
        parcel_geometry: Polygon,
    ) -> Distance | None:
        """Compute the distance from the parcel to the nearest object."""
        raise NotImplementedError

    @abstractmethod
    def nearest_object(
        self,
        objects: list[InfrastructureObject],
        parcel_geometry: Polygon,
    ) -> InfrastructureObject | None:
        """Return the object closest to the parcel, or ``None`` when there are none."""
        raise NotImplementedError

    @abstractmethod
    def coverage_ratio(
        self,
        objects: list[InfrastructureObject],
        buffer_zone: BufferZone,
    ) -> CoverageRatio:
        """Compute the coverage ratio of an objects in buffer zone."""
        raise NotImplementedError

    @abstractmethod
    def line_density(
        self,
        objects: list[InfrastructureObject],
        buffer_zone: BufferZone,
    ) -> Density:
        """Compute the total line length within the buffer per unit area."""
        raise NotImplementedError

    @abstractmethod
    def min_distance_to_large_object(
        self,
        objects: list[InfrastructureObject],
        parcel_geometry: Polygon,
        min_area_m2: float,
        always_large_ids: Iterable[str] = (),
    ) -> Distance | None:
        """Compute the distance to the nearest *large* object.

        Large objects are connected components whose area reaches
        ``min_area_m2``; non-areal objects (line features such as rivers) and
        objects whose id is listed in ``always_large_ids`` are always treated as
        large.
        """
        raise NotImplementedError


__all__ = ("InfrastructureMetricsService",)
