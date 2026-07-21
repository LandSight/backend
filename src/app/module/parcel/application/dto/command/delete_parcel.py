"""Delete parcel command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class DeleteParcelCommand:
    """Command for deleting a parcel.

    Attributes
    ----------
    parcel_id : UUID
        Parcel identifier.
    current_user_id : UUID
        ID of the user requesting the deletion (for ownership check).
    """

    parcel_id: UUID
    current_user_id: UUID


__all__ = ("DeleteParcelCommand",)
