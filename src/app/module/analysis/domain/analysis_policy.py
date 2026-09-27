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
        "hospital": 10_000,
        "grocery": 2_000,
        "bus_stop": 2_000,
        "railway_station": 3_000,
        "police": 2_000,
        "fire_station": 5_000,
        "pharmacy": 2_000,
        "water_source": 1_500,
        "water_body": 2_000,
        "forest": 1_500,
        "protected_area": 2_000,
        "power_line": 1_000,
        "road_accessibility": 2_000,
        "geographic_position": 150_000,
    },
)


__all__ = ("INFRASTRUCTURE_BUFFERS",)
