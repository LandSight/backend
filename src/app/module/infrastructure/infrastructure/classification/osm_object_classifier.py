"""OpenStreetMap implementation of the infrastructure object classifier."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.infrastructure.application.port import InfrastructureObjectClassifier
from app.module.infrastructure.domain.value_object import CityTier
from app.module.infrastructure.infrastructure.osm_tags import (
    MAIN_ROAD_CLASSES,
    PAVED_ROAD_CLASSES,
    PAVED_SURFACES,
    PLACE_TIERS,
    SIGNIFICANT_PROTECT_CLASSES,
)


if TYPE_CHECKING:
    from app.module.infrastructure.domain.entity import InfrastructureObject


class OsmInfrastructureObjectClassifier(InfrastructureObjectClassifier):
    """Classifies infrastructure objects using OpenStreetMap tags.

    This adapter is the only place in the module that knows OSM tag names, so
    the domain and application layers remain source-agnostic.
    """

    @override
    def city_tier(self, obj: InfrastructureObject) -> CityTier:
        """See :class:`app.module.infrastructure.application.port.InfrastructureObjectClassifier.city_tier`."""
        place = obj.tag("place")
        if place is None:
            return CityTier.UNKNOWN
        return PLACE_TIERS.get(place, CityTier.UNKNOWN)

    @override
    def is_paved_road(self, obj: InfrastructureObject) -> bool:
        """See :class:`app.module.infrastructure.application.port.InfrastructureObjectClassifier.is_paved_road`."""
        surface = obj.tag("surface")
        if surface is not None:
            return surface in PAVED_SURFACES
        return obj.tag("highway") in PAVED_ROAD_CLASSES

    @override
    def is_main_road(self, obj: InfrastructureObject) -> bool:
        """See :class:`app.module.infrastructure.application.port.InfrastructureObjectClassifier.is_main_road`."""
        return obj.tag("highway") in MAIN_ROAD_CLASSES

    @override
    def is_significant_protected_area(self, obj: InfrastructureObject) -> bool:
        """See :class:`app.module.infrastructure.application.port.InfrastructureObjectClassifier.is_significant_protected_area`."""
        return obj.tag("protect_class") in SIGNIFICANT_PROTECT_CLASSES


__all__ = ("OsmInfrastructureObjectClassifier",)
