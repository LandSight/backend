"""Delete restriction checks command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class DeleteRestrictionChecksCommand:
    """Command for deleting restriction check snapshots by their IDs.

    Attributes
    ----------
    check_ids : list[UUID]
        IDs of the snapshots to delete.
    current_user_id : UUID
        ID of the user performing the request; must own the checked parcels.
    """

    check_ids: list[UUID]
    current_user_id: UUID


__all__ = ("DeleteRestrictionChecksCommand",)
