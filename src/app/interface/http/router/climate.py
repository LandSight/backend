"""Climate module HTTP router."""

from __future__ import annotations

from litestar import Router

from app.interface.http.controller.climate.metrics import ClimateMetricsController


climate_router = Router(
    path="/climate",
    route_handlers=[
        ClimateMetricsController,
    ],
)

__all__ = ("climate_router",)
