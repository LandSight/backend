"""Get latest topography metrics command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetLatestParcelTopographyMetricsCommand:
    """Command for retrieving the most recent topography metrics for a parcel.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel to get the latest metrics for.
    """

    parcel_id: UUID


__all__ = ("GetLatestParcelTopographyMetricsCommand",)
