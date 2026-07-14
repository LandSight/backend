"""List user parcels command DTO."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ListUserParcelsCommand:
    """Command to list all parcels owned by a specific user.

    Attributes
    ----------
    owner_id : str
        Owner identifier.
    """

    owner_id: str


__all__ = ("ListUserParcelsCommand",)
