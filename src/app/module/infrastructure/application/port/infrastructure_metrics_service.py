"""Infrastructure metrics service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.domain.entity import InfrastructureObject
    from app.module.infrastructure.domain.value_object import (
        BufferZone,
        Count,
        CoverageRatio,
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
    def min_distance(
        self,
        objects: list[InfrastructureObject],
        parcel_geometry: Polygon,
    ) -> Distance | None:
        """Compute the distance from the parcel to the nearest object."""
        raise NotImplementedError

    @abstractmethod
    def coverage_ratio(
        self,
        objects: list[InfrastructureObject],
        buffer_zone: BufferZone,
    ) -> CoverageRatio:
        """Compute the coverage ratio of an objects in buffer zone."""
        raise NotImplementedError


__all__ = ("InfrastructureMetricsService",)
