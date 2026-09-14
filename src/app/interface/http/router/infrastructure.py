"""Infrastructure module HTTP router."""

from __future__ import annotations

from litestar import Router

from app.interface.http.controller.infrastructure.metrics import InfrastructureMetricsController


infrastructure_router = Router(
    path="/infrastructure",
    route_handlers=[
        InfrastructureMetricsController,
    ],
)

__all__ = ("infrastructure_router",)
