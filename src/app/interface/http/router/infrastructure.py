"""Infrastructure module HTTP router."""

from __future__ import annotations

from litestar import Router

from app.interface.http.controller.infrastructure.metrics import InfrastructureMetricsController
from app.interface.http.controller.infrastructure.objects import InfrastructureObjectsController


infrastructure_router = Router(
    path="/infrastructure",
    route_handlers=[
        InfrastructureMetricsController,
        InfrastructureObjectsController,
    ],
)

__all__ = ("infrastructure_router",)
