"""Analysis module HTTP router."""

from __future__ import annotations

from litestar import Router

from app.interface.http.controller.analysis.analysis import AnalysisController


analysis_router = Router(
    path="/analysis",
    route_handlers=[
        AnalysisController,
    ],
)

__all__ = ("analysis_router",)
