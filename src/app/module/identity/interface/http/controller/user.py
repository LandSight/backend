"""User profile endpoints."""

from litestar import get
from litestar.controller import Controller
from litestar.di import NamedDependency
from litestar.status_codes import HTTP_200_OK

from app.module.identity.application.dto.command import GetUserCommand
from app.module.identity.application.use_case import GetUserUseCase
from app.module.identity.interface.http.schema.user import UserResponse
from app.module.shared.application.dto.response import CurrentUser
from app.module.shared.interface.http.guards import require_authorization


class UserController(Controller):
    """User profile endpoints."""

    path = "/api/v1/users"
    tags = ("users",)
    guards = [require_authorization]  # noqa: RUF012

    @get(
        "/profile",
        status_code=HTTP_200_OK,
        description="Get the profile of the currently authenticated user.",
    )
    async def get_profile(
        self,
        get_user_use_case: NamedDependency[GetUserUseCase],
        current_user: CurrentUser,
    ) -> UserResponse:
        """Get the profile of the currently authenticated user.

        Parameters
        ----------
        get_user_use_case : GetUserUseCase
            Injected use case.
        current_user : CurrentUser
            The currently authenticated user (resolved from token).

        Returns
        -------
        UserResponse
            User profile data.
        """
        command = GetUserCommand(user_id=current_user.id)
        result = await get_user_use_case(command)
        return UserResponse(id=result.id, username=result.username)


__all__ = ("UserController",)
