"""Collect analysis restrictions command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class CollectRestrictionsCommand:
    """Command for the restriction-check phase of an analysis.

    Attributes
    ----------
    analysis_id : UUID
        ID of the analysis being processed.
    current_user_id : UUID
        ID of the user who requested the analysis.
    """

    analysis_id: UUID
    current_user_id: UUID


__all__ = ("CollectRestrictionsCommand",)
