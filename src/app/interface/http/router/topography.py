"""Topography module HTTP router."""

from __future__ import annotations

from litestar import Router

from app.interface.http.controller.topography.metrics import TopographyMetricsController


topography_router = Router(
    path="/topography",
    route_handlers=[
        TopographyMetricsController,
    ],
)

__all__ = ("topography_router",)
