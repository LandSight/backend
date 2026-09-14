"""Identity module HTTP router."""

from __future__ import annotations

from litestar import Router

from app.interface.http.controller.identity.auth import AuthController
from app.interface.http.controller.identity.user import UserController


identity_router = Router(
    path="/identity",
    route_handlers=[
        AuthController,
        UserController,
    ],
)

__all__ = ("identity_router",)
