"""Parcel HTTP schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.module.shared.interface.http.schema.geojson import (
    GeoJSONFeature,
    GeoJSONFeatureCollection,
    GeoJSONPolygon,
)


class CreateParcelRequest(BaseModel):
    """Request body for creating a parcel."""

    name: str = Field(
        description="Human-readable name of the parcel.",
        min_length=1,
        max_length=64,
    )
    polygon: GeoJSONPolygon = Field(
        description="Parcel geometry in GeoJSON Polygon format.",
    )


class ParcelFeatureProperties(BaseModel):
    """Properties of a parcel GeoJSON Feature."""

    id: str = Field(description="Parcel identifier.")
    name: str = Field(description="Human-readable name of the parcel.")
    owner_id: str = Field(description="ID of the user who owns this parcel.")


class ParcelFeature(GeoJSONFeature):
    """GeoJSON Feature for a parcel."""

    properties: ParcelFeatureProperties = Field(description="Parcel properties.")


class ParcelFeatureCollection(GeoJSONFeatureCollection):
    """GeoJSON FeatureCollection for a list of parcels."""

    features: list[ParcelFeature] = Field(description="List of parcel features.")


__all__ = (
    "CreateParcelRequest",
    "ParcelFeature",
    "ParcelFeatureCollection",
    "ParcelFeatureProperties",
)
