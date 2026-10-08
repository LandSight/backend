"""Value position value object."""

from __future__ import annotations

from enum import StrEnum


class ValuePosition(StrEnum):
    """Position of a raw metric value relative to its membership function zones.

    ``OPTIMAL``
        The value lies in the full-membership zone.
    ``PARTIAL_LOW``
        The value is below the optimal zone but still earns partial membership.
    ``PARTIAL_HIGH``
        The value is above the optimal zone but still earns partial membership.
    ``OUT_LOW``
        The value is at or below the lower zero-membership threshold.
    ``OUT_HIGH``
        The value is at or above the upper zero-membership threshold.
    ``UNKNOWN``
        The function, its parameters or the raw value are not available.
    """

    OPTIMAL = "optimal"
    PARTIAL_LOW = "partial_low"
    PARTIAL_HIGH = "partial_high"
    OUT_LOW = "out_low"
    OUT_HIGH = "out_high"
    UNKNOWN = "unknown"


__all__ = ("ValuePosition",)
