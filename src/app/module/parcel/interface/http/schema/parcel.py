"""Parcel HTTP schemas."""

from typing import Any

from pydantic import BaseModel, Field


class CreateParcelRequest(BaseModel):
    """Request body for creating a parcel."""

    name: str = Field(description="Human-readable name of the parcel.")
    polygon: dict[str, Any] = Field(
        description='GeoJSON Polygon geometry (e.g. ``{"type": "Polygon", "coordinates": [...]}``).',
    )


class ParcelResponse(BaseModel):
    """Response body for parcel data."""

    id: str = Field(description="Parcel identifier.")
    name: str = Field(description="Human-readable name of the parcel.")
    polygon: dict[str, Any] = Field(description="GeoJSON Polygon geometry.")
    owner_id: str = Field(description="ID of the user who owns this parcel.")


class ParcelListResponse(BaseModel):
    """Response body for a list of parcels."""

    parcels: list[ParcelResponse] = Field(description="List of parcels.")
    total: int = Field(description="Total number of parcels.")


__all__ = (
    "CreateParcelRequest",
    "ParcelListResponse",
    "ParcelResponse",
)
