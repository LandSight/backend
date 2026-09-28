"""Analysis module HTTP router."""

from __future__ import annotations

from litestar import Router

from app.interface.http.controller.analysis.analysis import AnalysisController
from app.interface.http.controller.analysis.catalog import AnalysisCatalogController


analysis_router = Router(
    path="/analysis",
    route_handlers=[
        AnalysisController,
    ],
)

analysis_catalog_router = Router(
    path="/",
    route_handlers=[
        AnalysisCatalogController,
    ],
)

__all__ = ("analysis_catalog_router", "analysis_router")
