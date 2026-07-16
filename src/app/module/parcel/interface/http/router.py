"""Parcel module HTTP router."""

from __future__ import annotations

from litestar import Router

from app.module.parcel.interface.http.controller.parcel import ParcelController


parcel_router = Router(
    path="/parcels",
    route_handlers=[
        ParcelController,
    ],
)

__all__ = ("parcel_router",)
