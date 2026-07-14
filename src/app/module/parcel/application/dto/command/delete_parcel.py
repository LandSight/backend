"""Delete parcel command."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeleteParcelCommand:
    """Command for deleting a parcel.

    Attributes
    ----------
    parcel_id : str
        Parcel identifier.
    """

    parcel_id: str


__all__ = ("DeleteParcelCommand",)
