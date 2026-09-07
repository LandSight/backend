"""Analyze parcel command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class AnalyzeParcelCommand:
    """Command for aggregating all metrics of a parcel.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel to aggregate metrics for.
    current_user_id : UUID
        ID of the user performing the request.
    """

    parcel_id: UUID
    current_user_id: UUID


__all__ = ("AnalyzeParcelCommand",)
