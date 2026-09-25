"""Start analysis command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.module.analysis.domain.value_object import AnalysisType


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
    analysis_type : AnalysisType
        Evaluation profile to run.
    """

    parcel_id: UUID
    current_user_id: UUID
    name: str
    analysis_type: AnalysisType = AnalysisType.IZHS


__all__ = ("StartAnalysisCommand",)
