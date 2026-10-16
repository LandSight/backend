"""Interpretation module HTTP router."""

from __future__ import annotations

from litestar import Router

from app.interface.http.controller.interpretation import InterpretationController


interpretation_router = Router(
    path="/analysis",
    route_handlers=[
        InterpretationController,
    ],
)

__all__ = ("interpretation_router",)
