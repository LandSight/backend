"""Centralized dependency injection for the HTTP layer.

Assembles module-level internal APIs and provides framework-level
dependencies (e.g., ``current_user``) that call into those APIs.
"""

from __future__ import annotations

from typing import Annotated

from litestar.di import Provide
from litestar.params import HeaderParameter

from app.interface.http.schema.current_user import CurrentUser
from app.module.climate.di import climate_dependencies
from app.module.identity.di import identity_dependencies
from app.module.identity.interface.internal.dto import GetCurrentUserByTokenInput
from app.module.identity.interface.internal.port import IdentityInternalAPI
from app.module.infrastructure.di import infrastructure_dependencies
from app.module.parcel.di import parcel_dependencies
from app.module.topography.di import topography_dependencies
from app.platform.di import platform_dependencies


#  Framework-level dependencies


async def provide_current_user(
    identity_api: IdentityInternalAPI,
    authorization: Annotated[str | None, HeaderParameter(name="Authorization")] = None,
) -> CurrentUser:
    """Resolve the current user from the Authorization header.

    Extracts the Bearer token from the header and delegates to the
    Identity module's internal API for token validation and user
    resolution.

    Parameters
    ----------
    identity_api : IdentityInternalAPI
        Injected identity internal API.
    authorization : str | None
        The raw Authorization header value, if present.

    Returns
    -------
    CurrentUser
        The authenticated user's id and username.

    Raises
    ------
    litestar.exceptions.NotAuthorizedException
        If the token is missing, invalid, or expired.
    """
    token = (authorization or "").removeprefix("Bearer ")
    result = await identity_api.get_current_user(GetCurrentUserByTokenInput(token=token))
    return CurrentUser(id=result.id, username=result.username)


def get_all_dependencies() -> dict[str, Provide]:
    """Merge all dependencies into a single dictionary.

    Returns
    -------
    dict[str, Provide]
        Combined dependencies dictionary.
    """
    dependencies: dict[str, Provide] = {}
    dependencies.update(platform_dependencies)
    dependencies.update(identity_dependencies)
    dependencies.update(parcel_dependencies)
    dependencies.update(topography_dependencies)
    dependencies.update(infrastructure_dependencies)
    dependencies.update(climate_dependencies)
    dependencies["current_user"] = Provide(provide_current_user)
    return dependencies


__all__ = (
    "get_all_dependencies",
    "provide_current_user",
)
