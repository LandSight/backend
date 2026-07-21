"""Parcel module HTTP router."""

from __future__ import annotations

from litestar import Router

from app.interface.http.controller.parcel.parcel import ParcelController


parcel_router = Router(
    path="/parcels",
    route_handlers=[
        ParcelController,
    ],
)

__all__ = ("parcel_router",)
