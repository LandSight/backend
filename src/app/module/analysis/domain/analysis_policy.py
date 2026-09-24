"""Static analysis policy defaults.

These are base analysis parameters, not environment-specific settings or
secrets, so they live in code as the single source of truth.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, Final


if TYPE_CHECKING:
    from collections.abc import Mapping


INFRASTRUCTURE_BUFFERS: Final[Mapping[str, int]] = MappingProxyType(
    {
        "hospital": 2000,
        "grocery": 500,
        "bus_stop": 500,
        "railway_station": 2000,
        "police": 2000,
        "fire_station": 2000,
        "pharmacy": 1000,
        "water_source": 1000,
        "water_body": 1500,
        "forest": 1000,
        "protected_area": 2000,
        "power_line": 1000,
        "road_accessibility": 1000,
        "geographic_position": 150000,
    },
)


__all__ = ("INFRASTRUCTURE_BUFFERS",)
