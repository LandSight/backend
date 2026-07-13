"""User profile endpoints."""

from typing import Annotated

from litestar import get
from litestar.controller import Controller
from litestar.di import NamedDependency
from litestar.params import HeaderParameter
from litestar.status_codes import HTTP_200_OK

from app.module.identity.application.dto.command import GetUserCommand
from app.module.identity.application.use_case import GetUserUseCase
from app.module.identity.interface.http.schema.user import UserResponse
from app.module.shared.application.port import CurrentUserProvider


class UserController(Controller):
    """User profile endpoints."""

    path = "/api/v1/users"
    tags = ("users",)

    @get(
        "/profile",
        status_code=HTTP_200_OK,
        description="Get the profile of the currently authenticated user.",
    )
    async def get_profile(
        self,
        get_user_use_case: NamedDependency[GetUserUseCase],
        current_user_provider: NamedDependency[CurrentUserProvider],
        authorization: Annotated[str, HeaderParameter(name="Authorization", required=True)],
    ) -> UserResponse:
        """Get the profile of the currently authenticated user.

        Parameters
        ----------
        get_user_use_case : GetUserUseCase
            Injected use case.
        current_user_provider : CurrentUserProvider
            Injected provider for extracting user ID from the token.
        authorization : str | None
            Raw Authorization header value (injected by Litestar via Parameter).

        Returns
        -------
        UserResponse
            User profile data.
        """
        token = (authorization or "").removeprefix("Bearer ")
        current_user_id = await current_user_provider.get_current_user_id(token)
        command = GetUserCommand(user_id=current_user_id)
        result = await get_user_use_case(command)
        return UserResponse(id=result.id, username=result.username)


__all__ = ("UserController",)
