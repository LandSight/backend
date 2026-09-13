"""List user analyses command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class ListUserAnalysesCommand:
    """Command for listing all analyses of a user across all statuses.

    Attributes
    ----------
    current_user_id : UUID
        ID of the user whose analyses are listed.
    """

    current_user_id: UUID


__all__ = ("ListUserAnalysesCommand",)
