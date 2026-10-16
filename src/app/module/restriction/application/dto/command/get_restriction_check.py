"""Get restriction check command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetRestrictionCheckCommand:
    """Command for retrieving a restriction check snapshot by its ID.

    Attributes
    ----------
    check_id : UUID
        ID of the restriction check snapshot.
    current_user_id : UUID
        ID of the user performing the request.
    """

    check_id: UUID
    current_user_id: UUID


__all__ = ("GetRestrictionCheckCommand",)
