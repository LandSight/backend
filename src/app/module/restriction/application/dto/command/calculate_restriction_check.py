"""Calculate restriction check command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class CalculateRestrictionCheckCommand:
    """Command for calculating the restriction check of a parcel.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel to check.
    current_user_id : UUID
        ID of the user performing the request.
    """

    parcel_id: UUID
    current_user_id: UUID


__all__ = ("CalculateRestrictionCheckCommand",)
