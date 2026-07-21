"""Get user command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetUserCommand:
    """Command for retrieving a user by ID.

    Attributes
    ----------
    user_id : UUID
        User identifier.
    """

    user_id: UUID


__all__ = ("GetUserCommand",)
