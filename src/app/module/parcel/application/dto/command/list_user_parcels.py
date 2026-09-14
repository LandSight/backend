"""List user parcels command DTO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class ListUserParcelsCommand:
    """Command to list all parcels owned by a specific user.

    Attributes
    ----------
    owner_id : UUID
        Owner identifier.
    """

    owner_id: UUID


__all__ = ("ListUserParcelsCommand",)
