"""Infrastructure object category value object."""

from __future__ import annotations

from enum import StrEnum


class Category(StrEnum):
    """Category of infrastructure metrics.

    A category identifies the kind of object or feature a metrics row is
    computed for. Categories that share the same metric shape are stored in a
    common family table and are disambiguated by a type column.
    """

    HOSPITAL = "hospital"
    GROCERY = "grocery"
    BUS_STOP = "bus_stop"
    RAILWAY_STATION = "railway_station"
    POLICE = "police"
    FIRE_STATION = "fire_station"
    PHARMACY = "pharmacy"
    WATER_SOURCE = "water_source"
    WATER_BODY = "water_body"
    FOREST = "forest"
    PROTECTED_AREA = "protected_area"
    POWER_LINE = "power_line"
    ROAD_ACCESSIBILITY = "road_accessibility"
    GEOGRAPHIC_POSITION = "geographic_position"


__all__ = ("Category",)
