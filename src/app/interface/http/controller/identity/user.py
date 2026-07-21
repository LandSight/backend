"""User profile HTTP endpoints."""

from __future__ import annotations

from litestar import get
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK

from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.schema.identity import UserResponse
from app.interface.http.util.guards import require_authorization


class UserController(Controller):
    """User profile endpoints."""

    path = "/users"
    tags = ("users",)
    guards = [require_authorization]

    @get(
        "/profile",
        status_code=HTTP_200_OK,
        description="Get the profile of the currently authenticated user.",
    )
    async def get_profile(
        self,
        current_user: CurrentUser,
    ) -> UserResponse:
        """Get the profile of the currently authenticated user."""
        return UserResponse(id=current_user.id, username=current_user.username)


__all__ = ("UserController",)
