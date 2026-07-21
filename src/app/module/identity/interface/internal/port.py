"""Port (abstract base) for the Identity module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.identity.interface.internal.dto import (
        GetCurrentUserByTokenInput,
        GetUserInput,
        LoginInput,
        RefreshTokenInput,
        RegisterUserInput,
        TokenResult,
        UserResult,
    )


class IdentityInternalAPI(ABC):
    """Abstract interface for the Identity module's internal API.

    This is the framework-agnostic contract that the HTTP layer
    (``app/interface/http/controller/identity/``) depends on.

    Implementations:
    - :class:`app.module.identity.interface.internal.api.IdentityInternal`
    """

    @abstractmethod
    async def register(self, input_data: RegisterUserInput) -> UserResult:
        """Register a new user."""
        raise NotImplementedError

    @abstractmethod
    async def login(self, input_data: LoginInput) -> TokenResult:
        """Authenticate a user and return tokens."""
        raise NotImplementedError

    @abstractmethod
    async def refresh_token(self, input_data: RefreshTokenInput) -> TokenResult:
        """Refresh an access token using a refresh token."""
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, input_data: GetUserInput) -> UserResult:
        """Get a user by ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_current_user(self, input_data: GetCurrentUserByTokenInput) -> UserResult:
        """Resolve the current user from an authentication token."""
        raise NotImplementedError


__all__ = ("IdentityInternalAPI",)
