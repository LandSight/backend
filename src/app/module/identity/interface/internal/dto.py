"""Internal DTOs for the Identity module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class RegisterUserInput:
    """Input for registering a new user."""

    username: str
    password: str


@dataclass(frozen=True, slots=True)
class LoginInput:
    """Input for authenticating a user."""

    username: str
    password: str


@dataclass(frozen=True, slots=True)
class RefreshTokenInput:
    """Input for refreshing an access token."""

    refresh_token: str


@dataclass(frozen=True, slots=True)
class GetUserInput:
    """Input for retrieving a user by ID."""

    user_id: UUID


@dataclass(frozen=True, slots=True)
class GetCurrentUserByTokenInput:
    """Input for resolving the current user from a token."""

    token: str


@dataclass(frozen=True, slots=True)
class TokenResult:
    """Result of authentication / token refresh."""

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"  # noqa: S105


@dataclass(frozen=True, slots=True)
class UserResult:
    """Result of user retrieval / registration."""

    id: UUID
    username: str


__all__ = (
    "GetCurrentUserByTokenInput",
    "GetUserInput",
    "LoginInput",
    "RefreshTokenInput",
    "RegisterUserInput",
    "TokenResult",
    "UserResult",
)
