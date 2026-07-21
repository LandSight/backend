"""User response DTO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class UserResponse:
    """DTO for user data returned from use cases.

    Attributes
    ----------
    id : UUID
        User identifier.
    username : str
        Username.
    """

    id: UUID
    username: str


__all__ = ("UserResponse",)
