"""Aspect direction enum."""

from __future__ import annotations

from enum import StrEnum


class AspectDirection(StrEnum):
    """Cardinal and intercardinal directions for slope aspect.

    Values represent the direction a slope faces, measured clockwise
    from north in degrees, mapped to compass directions.
    """

    N = "N"  # 0°
    NE = "NE"  # 45°
    E = "E"  # 90°
    SE = "SE"  # 135°
    S = "S"  # 180°
    SW = "SW"  # 225°
    W = "W"  # 270°
    NW = "NW"  # 315°
    FLAT = "FLAT"  # No slope


__all__ = ("AspectDirection",)
