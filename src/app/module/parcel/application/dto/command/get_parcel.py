"""Get parcel command."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetParcelCommand:
    """Command for retrieving a parcel by ID.

    Attributes
    ----------
    parcel_id : str
        Parcel identifier.
    """

    parcel_id: str


__all__ = ("GetParcelCommand",)
