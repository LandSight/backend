"""Dependency assembly for the application."""

from typing import Annotated

from litestar.di import Provide
from litestar.params import HeaderParameter

from app.module.identity.di import identity_dependencies
from app.module.parcel.di import parcel_dependencies
from app.module.shared.application.dto.response import CurrentUser  # noqa: TC001
from app.module.shared.application.port import CurrentUserProvider  # noqa: TC001
from app.platform.di import platform_dependencies


async def provide_current_user(
    current_user_provider: CurrentUserProvider,
    authorization: Annotated[str | None, HeaderParameter(name="Authorization")] = None,
) -> CurrentUser:
    """Resolve the current user from the Authorization header.

    This dependency is automatically available to all route handlers
    that declare a ``current_user`` parameter. It extracts the Bearer
    token from the header and delegates to ``CurrentUserProvider`` for
    token validation and user resolution.

    Parameters
    ----------
    current_user_provider : CurrentUserProvider
        Injected port for resolving the current user.
    authorization : str | None
        The raw Authorization header value, if present.

    Returns
    -------
    CurrentUser
        The authenticated user's id and username.

    Raises
    ------
    litestar.exceptions.NotAuthorizedException
        If the token is missing, invalid, or expired (via exception handler).
    """
    token = (authorization or "").removeprefix("Bearer ")
    return await current_user_provider.get_current_user(token)


def get_all_dependencies() -> dict[str, Provide]:
    """Merge all module dependencies into a single dictionary.

    Returns
    -------
    dict[str, Provide]
        Combined dependencies dictionary.
    """
    dependencies = {}
    dependencies.update(platform_dependencies)
    dependencies.update(identity_dependencies)
    dependencies.update(parcel_dependencies)
    dependencies["current_user"] = Provide(provide_current_user)
    return dependencies
