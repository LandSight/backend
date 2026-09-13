"""Delete analysis command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class DeleteAnalysisCommand:
    """Command for deleting an analysis.

    Attributes
    ----------
    analysis_id : UUID
        ID of the analysis to delete.
    current_user_id : UUID
        ID of the user performing the request.
    """

    analysis_id: UUID
    current_user_id: UUID


__all__ = ("DeleteAnalysisCommand",)
