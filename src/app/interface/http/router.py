"""API v1 router.

Groups all module routers under the ``/api/v1`` prefix.
"""

from __future__ import annotations

from litestar import Router

from app.module.identity.interface.http.router import identity_router
from app.module.parcel.interface.http.router import parcel_router


api_v1_router = Router(
    path="/api/v1",
    route_handlers=[
        identity_router,
        parcel_router,
    ],
)

__all__ = ("api_v1_router",)
