"""List topography metrics command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class ListParcelTopographyMetricsCommand:
    """Command for listing all topography metrics snapshots for a parcel.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel whose metrics history to list.
    current_user_id : UUID
        ID of the user performing the request.
    """

    parcel_id: UUID
    current_user_id: UUID


__all__ = ("ListParcelTopographyMetricsCommand",)
