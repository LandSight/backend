"""Delete parcel command."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeleteParcelCommand:
    """Command for deleting a parcel.

    Attributes
    ----------
    parcel_id : str
        Parcel identifier.
    current_user_id : str
        ID of the user requesting the deletion (for ownership check).
    """

    parcel_id: str
    current_user_id: str


__all__ = ("DeleteParcelCommand",)
