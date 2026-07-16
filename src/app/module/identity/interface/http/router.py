"""Identity module HTTP router."""

from __future__ import annotations

from litestar import Router

from app.module.identity.interface.http.controller.auth import AuthController
from app.module.identity.interface.http.controller.user import UserController


identity_router = Router(
    path="/identity",
    route_handlers=[
        AuthController,
        UserController,
    ],
)

__all__ = ("identity_router",)
