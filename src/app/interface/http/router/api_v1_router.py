"""API v1 router.

Groups all module routers under the ``/api/v1`` prefix.
"""

from __future__ import annotations

from litestar import Router

from app.interface.http.router.identity import identity_router
from app.interface.http.router.parcel import parcel_router
from app.interface.http.router.topography import topography_router


api_v1_router = Router(
    path="/api/v1",
    route_handlers=[
        identity_router,
        parcel_router,
        topography_router,
    ],
)

__all__ = ("api_v1_router",)
