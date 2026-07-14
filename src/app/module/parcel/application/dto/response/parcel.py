"""Parcel response DTO."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ParcelResponse:
    """Response DTO for a parcel.

    Attributes
    ----------
    id : str
        Parcel identifier.
    name : str
        Human-readable name of the parcel.
    polygon : dict
        GeoJSON Polygon geometry.
    owner_id : str
        ID of the user who owns this parcel.
    """

    id: str
    name: str
    polygon: dict
    owner_id: str


__all__ = ("ParcelResponse",)
