"""Guards for the application."""

from __future__ import annotations

from typing import TYPE_CHECKING

from litestar.exceptions import NotAuthorizedException


if TYPE_CHECKING:
    from litestar.connection import ASGIConnection
    from litestar.handlers.base import BaseRouteHandler


async def require_authorization(
    connection: ASGIConnection,
    _handler: BaseRouteHandler,
) -> None:
    """Guard that checks for the presence of an Authorization header.

    This guard is applied globally to all routes. It only checks that
    the header *exists* — it does NOT validate the token itself.
    Token validation is handled by the ``current_user`` dependency.

    Routes that should not require authentication (e.g., login, register)
    must override the guard list with an empty list::

        class AuthController(Controller):
            guards = []

    Parameters
    ----------
    connection : ASGIConnection
        The incoming connection (request or websocket).
    _handler : BaseRouteHandler
        The route handler being guarded.

    Raises
    ------
    NotAuthorizedException
        If the Authorization header is missing.
    """
    auth_header = connection.headers.get("Authorization")
    if not auth_header:
        message = "Authorization header is required"
        raise NotAuthorizedException(message)


__all__ = ("require_authorization",)
