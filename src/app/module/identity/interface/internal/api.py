"""Concrete implementation of the Identity module's internal API.

See :class:`app.module.identity.interface.internal.port.IdentityInternalAPI`
for the abstract interface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.identity.application.dto.command import (
    AuthenticateUserCommand,
    GetCurrentUserByTokenCommand,
    GetUserCommand,
    RefreshTokenCommand,
    RegisterUserCommand,
)
from app.module.identity.interface.internal.dto import (
    GetCurrentUserByTokenInput,
    GetUserInput,
    LoginInput,
    RefreshTokenInput,
    RegisterUserInput,
    TokenResult,
    UserResult,
)
from app.module.identity.interface.internal.port import IdentityInternalAPI


if TYPE_CHECKING:
    from app.module.identity.application.use_case import (
        AuthenticateUserUseCase,
        GetCurrentUserByTokenUseCase,
        GetUserUseCase,
        RefreshTokenUseCase,
        RegisterUserUseCase,
    )


class IdentityInternal(IdentityInternalAPI):
    """Concrete implementation of the Identity internal API.

    Wraps the application-layer use cases into a single cohesive
    interface that the HTTP layer calls.
    """

    def __init__(
        self,
        register_use_case: RegisterUserUseCase,
        authenticate_use_case: AuthenticateUserUseCase,
        refresh_token_use_case: RefreshTokenUseCase,
        get_user_use_case: GetUserUseCase,
        get_current_user_by_token_use_case: GetCurrentUserByTokenUseCase,
    ) -> None:
        self._register = register_use_case
        self._authenticate = authenticate_use_case
        self._refresh = refresh_token_use_case
        self._get_user = get_user_use_case
        self._get_current_user_by_token = get_current_user_by_token_use_case

    @override
    async def register(self, input_data: RegisterUserInput) -> UserResult:
        """See :meth:`IdentityInternalAPI.register`."""
        result = await self._register(
            RegisterUserCommand(
                username=input_data.username,
                password=input_data.password,
            )
        )
        return UserResult(id=result.id, username=result.username)

    @override
    async def login(self, input_data: LoginInput) -> TokenResult:
        """See :meth:`IdentityInternalAPI.login`."""
        result = await self._authenticate(
            AuthenticateUserCommand(
                username=input_data.username,
                password=input_data.password,
            )
        )
        return TokenResult(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
        )

    @override
    async def refresh_token(self, input_data: RefreshTokenInput) -> TokenResult:
        """See :meth:`IdentityInternalAPI.refresh_token`."""
        result = await self._refresh(RefreshTokenCommand(refresh_token=input_data.refresh_token))
        return TokenResult(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
        )

    @override
    async def get_user(self, input_data: GetUserInput) -> UserResult:
        """See :meth:`IdentityInternalAPI.get_user`."""
        result = await self._get_user(GetUserCommand(user_id=input_data.user_id))
        return UserResult(id=result.id, username=result.username)

    @override
    async def get_current_user(self, input_data: GetCurrentUserByTokenInput) -> UserResult:
        """See :meth:`IdentityInternalAPI.get_current_user`."""
        result = await self._get_current_user_by_token(GetCurrentUserByTokenCommand(token=input_data.token))
        return UserResult(id=result.id, username=result.username)


__all__ = ("IdentityInternal",)
