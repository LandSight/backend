"""Get analysis command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetAnalysisCommand:
    """Command for retrieving an analysis by its ID.

    Attributes
    ----------
    analysis_id : UUID
        ID of the analysis to retrieve.
    current_user_id : UUID
        ID of the user performing the request.
    """

    analysis_id: UUID
    current_user_id: UUID


__all__ = ("GetAnalysisCommand",)
