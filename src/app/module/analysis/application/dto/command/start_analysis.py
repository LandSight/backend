"""Start analysis command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class StartAnalysisCommand:
    """Command for starting an analysis of a parcel.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel to analyse.
    current_user_id : UUID
        ID of the user performing the request.
    name : str
        Human-readable name of the analysis.
    """

    parcel_id: UUID
    current_user_id: UUID
    name: str


__all__ = ("StartAnalysisCommand",)
