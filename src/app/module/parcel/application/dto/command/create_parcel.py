"""Create parcel command."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateParcelCommand:
    """Command for creating a new parcel.

    Attributes
    ----------
    name : str
        Human-readable name of the parcel.
    polygon : dict
        GeoJSON Polygon geometry.
    owner_id : str
        ID of the user who owns this parcel.
    """

    name: str
    polygon: dict
    owner_id: str


__all__ = ("CreateParcelCommand",)
