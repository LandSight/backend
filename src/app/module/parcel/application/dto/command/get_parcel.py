"""Get parcel command."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetParcelCommand:
    """Command for retrieving a parcel by ID.

    Attributes
    ----------
    parcel_id : str
        Parcel identifier.
    current_user_id : str
        ID of the user requesting the parcel (for ownership check).
    """

    parcel_id: str
    current_user_id: str


__all__ = ("GetParcelCommand",)
