"""Get analysis evaluation command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetAnalysisEvaluationCommand:
    """Command for retrieving the stored evaluation of an analysis.

    Attributes
    ----------
    analysis_id : UUID
        ID of the analysis to retrieve the evaluation for.
    current_user_id : UUID
        ID of the requesting user.
    """

    analysis_id: UUID
    current_user_id: UUID


__all__ = ("GetAnalysisEvaluationCommand",)
