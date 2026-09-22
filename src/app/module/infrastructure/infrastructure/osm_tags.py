"""OpenStreetMap tag vocabulary used by the Infrastructure adapters.

This module is the single place that knows which OSM tag values the module
relies on, so the tag filters (repository) and the object classification
adapter share one vocabulary instead of each keeping its own copy.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, Final

from app.module.infrastructure.domain.value_object import CityTier


if TYPE_CHECKING:
    from collections.abc import Mapping

# Values of ``shop=*`` that count as a grocery shop.
GROCERY_SHOPS: Final[tuple[str, ...]] = (
    "supermarket",
    "convenience",
    "greengrocer",
    "bakery",
    "butcher",
    "grocery",
    "farm",
    "deli",
)

# Values of ``highway=*`` that count as a paved road.
PAVED_ROAD_CLASSES: Final[tuple[str, ...]] = (
    "motorway",
    "trunk",
    "primary",
    "secondary",
    "tertiary",
)

# Values of ``place=*`` that count as a major settlement.
MAJOR_SETTLEMENT_PLACES: Final[tuple[str, ...]] = ("city", "town")

# Values of ``railway=*`` that count as a railway station.
RAILWAY_STATION_KINDS: Final[tuple[str, ...]] = ("station", "halt")

# Values of ``power=*`` that count as a power line.
POWER_LINE_KINDS: Final[tuple[str, ...]] = ("line", "minor_line")

# Values of ``surface=*`` that mean a road is not paved.
UNPAVED_SURFACES: Final[tuple[str, ...]] = (
    "unpaved",
    "gravel",
    "ground",
    "dirt",
    "sand",
    "grass",
    "earth",
    "compacted",
)

# Values of ``protect_class=*`` that make a protected area significant
# regardless of its measured area.
SIGNIFICANT_PROTECT_CLASSES: Final[tuple[str, ...]] = ("1", "1a", "1b", "2", "3", "4")

# Mapping of ``place=*`` values onto settlement tiers.
PLACE_TIERS: Final[Mapping[str, CityTier]] = MappingProxyType(
    {
        "city": CityTier.REGIONAL_CENTER,
        "town": CityTier.DISTRICT_CENTER,
        "village": CityTier.LOCAL_TOWN,
        "hamlet": CityTier.LOCAL_TOWN,
    },
)


__all__ = (
    "GROCERY_SHOPS",
    "MAJOR_SETTLEMENT_PLACES",
    "PAVED_ROAD_CLASSES",
    "PLACE_TIERS",
    "POWER_LINE_KINDS",
    "RAILWAY_STATION_KINDS",
    "SIGNIFICANT_PROTECT_CLASSES",
    "UNPAVED_SURFACES",
)
