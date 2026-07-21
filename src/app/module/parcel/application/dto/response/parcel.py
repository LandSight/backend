"""Parcel response DTO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class ParcelResponse:
    """Response DTO for a parcel.

    Attributes
    ----------
    id : UUID
        Parcel identifier.
    name : str
        Human-readable name of the parcel.
    polygon : dict
        GeoJSON Polygon geometry.
    owner_id : UUID
        ID of the user who owns this parcel.
    """

    id: UUID
    name: str
    polygon: dict
    owner_id: UUID


__all__ = ("ParcelResponse",)
