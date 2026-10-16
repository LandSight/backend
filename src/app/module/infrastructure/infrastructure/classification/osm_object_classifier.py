"""OpenStreetMap implementation of the infrastructure object classifier."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.infrastructure.application.port import InfrastructureObjectClassifier
from app.module.infrastructure.domain.value_object import CityTier
from app.module.infrastructure.infrastructure.osm_tags import (
    DEFAULT_POWER_LINE_VOLTAGE_KV,
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

    _VOLTS_PER_KV = 1000.0

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

    @override
    def power_line_voltage_kv(self, obj: InfrastructureObject) -> float:
        """See :class:`app.module.infrastructure.application.port.InfrastructureObjectClassifier.power_line_voltage_kv`."""
        voltages_kv = [
            float(value) / self._VOLTS_PER_KV
            for value in (obj.tag("voltage") or "").split(";")
            if self._is_number(value.strip())
        ]
        if voltages_kv:
            return max(voltages_kv)
        return DEFAULT_POWER_LINE_VOLTAGE_KV.get(obj.tag("power") or "", DEFAULT_POWER_LINE_VOLTAGE_KV["line"])

    @staticmethod
    def _is_number(value: str) -> bool:
        """Return whether a tag value is a plain non-negative number."""
        try:
            return float(value) >= 0
        except ValueError:
            return False


__all__ = ("OsmInfrastructureObjectClassifier",)
