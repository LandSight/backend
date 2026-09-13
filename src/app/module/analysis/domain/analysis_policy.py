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
        "school": 1000,
        "hospital": 2000,
        "shop": 500,
        "transit_stop": 500,
        "water_body": 2000,
    },
)


__all__ = ("INFRASTRUCTURE_BUFFERS",)
