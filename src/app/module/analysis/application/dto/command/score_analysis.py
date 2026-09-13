"""Score analysis command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class ScoreAnalysisCommand:
    """Command for the scoring phase of an analysis.

    Attributes
    ----------
    analysis_id : UUID
        ID of the analysis to score.
    current_user_id : UUID
        ID of the user who requested the analysis.
    """

    analysis_id: UUID
    current_user_id: UUID


__all__ = ("ScoreAnalysisCommand",)
