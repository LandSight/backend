"""Static infrastructure metric policy.

Thresholds that define what counts as a *large* natural object per category,
and the regulatory protection zones of overhead power lines. These are base
domain parameters, not environment-specific settings, so they live in code as
the single source of truth.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, Final

from app.module.infrastructure.domain.value_object import Category


if TYPE_CHECKING:
    from collections.abc import Mapping


LARGE_OBJECT_MIN_AREA_M2: Final[Mapping[Category, float]] = MappingProxyType(
    {
        Category.WATER_BODY: 1_000_000.0,
        Category.FOREST: 500_000.0,
        Category.PROTECTED_AREA: 1_000_000.0,
    },
)


# Voltage from which an overhead line is a transmission line: a building
# constraint rather than a connection opportunity for a house.
TRANSMISSION_LINE_MIN_VOLTAGE_KV: Final[float] = 35.0

# Protection zone half-width around an overhead line, measured from its axis,
# by upper voltage bound in kV. The Russian rule (Government Decree No. 160 of
# 24.02.2009) measures the zone from the outermost wire: up to 1 kV 2 m,
# 1-20 kV 10 m, 35 kV 15 m, 110 kV 20 m, 150-220 kV 25 m, 300-500 kV 30 m,
# 750 kV 40 m, 1150 kV 55 m. OSM maps the axis, so half of a typical
# crossarm span is added. No residential building is allowed in the zone.
_POWER_LINE_PROTECTION_ZONES_M: Final[tuple[tuple[float, float], ...]] = (
    (1.0, 3.0),
    (20.0, 12.0),
    (35.0, 18.0),
    (110.0, 25.0),
    (220.0, 30.0),
    (500.0, 40.0),
    (750.0, 55.0),
)
_POWER_LINE_MAX_PROTECTION_ZONE_M: Final[float] = 75.0


def power_line_protection_zone_m(voltage_kv: float) -> float:
    """Return the protection zone half-width of an overhead line, from its axis, in meters."""
    for max_voltage_kv, zone_m in _POWER_LINE_PROTECTION_ZONES_M:
        if voltage_kv <= max_voltage_kv:
            return zone_m
    return _POWER_LINE_MAX_PROTECTION_ZONE_M


__all__ = (
    "LARGE_OBJECT_MIN_AREA_M2",
    "TRANSMISSION_LINE_MIN_VOLTAGE_KV",
    "power_line_protection_zone_m",
)
