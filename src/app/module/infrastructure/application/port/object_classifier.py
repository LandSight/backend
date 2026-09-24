"""Infrastructure object classifier port.

The classifier translates source-specific attributes of a raw infrastructure
object into domain concepts. Keeping it behind a port means the domain and the
application layers stay free of data source specifics (such as OpenStreetMap
tag names), which live only in the adapter.

Implementations:
- :class:`app.module.infrastructure.infrastructure.classification.osm_object_classifier.OsmInfrastructureObjectClassifier`
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.domain.entity import InfrastructureObject
    from app.module.infrastructure.domain.value_object import CityTier


class InfrastructureObjectClassifier(ABC):
    """Port for source-specific classification of infrastructure objects."""

    @abstractmethod
    def city_tier(self, obj: InfrastructureObject) -> CityTier:
        """Return the settlement tier of a major city object."""
        raise NotImplementedError

    @abstractmethod
    def is_paved_road(self, obj: InfrastructureObject) -> bool:
        """Return whether a road object has a paved surface."""
        raise NotImplementedError

    @abstractmethod
    def is_main_road(self, obj: InfrastructureObject) -> bool:
        """Return whether a road object is a main (trunk or primary) road."""
        raise NotImplementedError

    @abstractmethod
    def is_significant_protected_area(self, obj: InfrastructureObject) -> bool:
        """Return whether a protected area is significant regardless of its area."""
        raise NotImplementedError


__all__ = ("InfrastructureObjectClassifier",)
