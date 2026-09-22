"""Infrastructure object category value object."""

from __future__ import annotations

from enum import StrEnum


class Category(StrEnum):
    """Category of infrastructure metrics."""

    SCHOOL = "school"
    HOSPITAL = "hospital"
    GROCERY = "grocery"
    BUS_STOP = "bus_stop"
    RAILWAY_STATION = "railway_station"
    WATER_BODY = "water_body"
    FOREST = "forest"
    PROTECTED_AREA = "protected_area"
    POWER_LINE = "power_line"
    GAS_PIPELINE = "gas_pipeline"
    WATER_PIPELINE = "water_pipeline"
    ROAD_ACCESSIBILITY = "road_accessibility"
    GEOGRAPHIC_POSITION = "geographic_position"


__all__ = ("Category",)
