"""Calculate topography metrics command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class CalculateTopographyMetricsCommand:
    """Command for calculating topography metrics for a parcel.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel to calculate metrics for.
    polygon : dict
        GeoJSON Polygon geometry defining the area of interest.
    """

    parcel_id: UUID
    polygon: dict


__all__ = ("CalculateTopographyMetricsCommand",)
