"""Get topography metrics command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetTopographyMetricsCommand:
    """Command for retrieving topography metrics by parcel ID.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel to get metrics for.
    """

    parcel_id: UUID


__all__ = ("GetTopographyMetricsCommand",)
