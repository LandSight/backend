"""Restriction kind value object."""

from __future__ import annotations

from enum import StrEnum


class RestrictionKind(StrEnum):
    """Kind of zone that restricts the use of land.

    Zones are facts: a regulatory buffer around an object or the object itself.
    Widths and legal grounds are in ``etl/zones.yaml`` and ``docs/restrictions.md``.
    """

    PROTECTED_AREA = "protected_area"
    PROTECTED_AREA_BUFFER = "protected_area_buffer"
    POWER_LINE_ZONE = "power_line_zone"
    GAS_DISTRIBUTION_ZONE = "gas_distribution_zone"
    TRUNK_PIPELINE_ZONE = "trunk_pipeline_zone"
    TRUNK_PIPELINE_MIN_DISTANCE = "trunk_pipeline_min_distance"
    RAILWAY_STRIP = "railway_strip"
    RAILWAY_SANITARY_GAP = "railway_sanitary_gap"
    ROAD_BODY = "road_body"
    ROADSIDE_STRIP = "roadside_strip"
    WATER_BODY = "water_body"
    SHORE_STRIP = "shore_strip"
    COASTAL_PROTECTION_STRIP = "coastal_protection_strip"
    WATER_PROTECTION_ZONE = "water_protection_zone"
    WETLAND = "wetland"
    CEMETERY = "cemetery"
    CEMETERY_SZZ = "cemetery_szz"
    LANDFILL = "landfill"
    LANDFILL_SZZ = "landfill_szz"
    WASTEWATER_SZZ = "wastewater_szz"
    INDUSTRIAL = "industrial"
    INDUSTRIAL_BUFFER = "industrial_buffer"
    AIRFIELD = "airfield"
    AIRFIELD_VICINITY = "airfield_vicinity"
    MILITARY = "military"
    PRISON = "prison"
    PRISON_BUFFER = "prison_buffer"


__all__ = ("RestrictionKind",)
