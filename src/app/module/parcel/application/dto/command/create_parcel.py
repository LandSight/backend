"""Create parcel command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.shared.application.dto.geojson import GeoJSONPolygon


@dataclass(frozen=True, slots=True)
class CreateParcelCommand:
    """Command for creating a new parcel.

    Attributes
    ----------
    name : str
        Human-readable name of the parcel.
    polygon : GeoJSONPolygon
        GeoJSON Polygon geometry.
    owner_id : UUID
        ID of the user who owns this parcel.
    """

    name: str
    polygon: GeoJSONPolygon
    owner_id: UUID


__all__ = ("CreateParcelCommand",)
