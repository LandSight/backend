"""Topography HTTP schemas (Pydantic)."""

from __future__ import annotations

import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.interface.http.schema.geojson import GeoJSONPolygon


class CalculateTopographyMetricsRequest(BaseModel):
    """Request body for calculating topography metrics."""

    parcel_id: UUID = Field(
        description="ID of the parcel to calculate metrics for.",
    )
    polygon: GeoJSONPolygon = Field(
        description="Parcel geometry in GeoJSON Polygon format.",
    )


class TopographyMetricsResponse(BaseModel):
    """Response body for topography metrics."""

    id: UUID = Field(description="Topography metrics identifier.")
    parcel_id: UUID = Field(description="ID of the parcel these metrics belong to.")
    created_at: datetime.datetime | None = Field(description="When these metrics were created (UTC).")
    mean_elevation: float = Field(description="Mean elevation in meters.")
    max_elevation: float = Field(description="Maximum elevation in meters.")
    min_elevation: float = Field(description="Minimum elevation in meters.")
    elevation_range: float = Field(description="Elevation range (max - min) in meters.")
    elevation_std: float = Field(description="Standard deviation of elevation in meters.")
    mean_slope: float = Field(description="Mean slope in degrees.")
    max_slope: float = Field(description="Maximum slope in degrees.")
    slope_percentiles: dict[int, float] = Field(
        default_factory=dict,
        description="Slope values at percentiles 25, 50, 75, 90.",
    )
    slope_distribution: list[float] = Field(
        default_factory=list,
        description="Slope histogram bins (10 bins, 0-90°).",
    )
    aspect: str = Field(default="", description="Dominant slope aspect direction.")
    south_aspect_percentage: float = Field(
        default=0.0,
        description="Percentage of area facing south (SE, S, SW).",
    )
    area: float = Field(default=0.0, description="Parcel area in square meters.")
    perimeter: float = Field(default=0.0, description="Parcel perimeter in meters.")
    compactness_index: float = Field(
        default=0.0,
        description="Compactness index (4πA/P²), dimensionless.",
    )
    elongation_index: float = Field(
        default=0.0,
        description="Elongation index (width/length), dimensionless.",
    )


class TopographyMetricsHistoryResponse(BaseModel):
    """Response body listing topography metrics snapshots for a parcel."""

    items: list[TopographyMetricsResponse] = Field(
        default_factory=list,
        description="Topography metrics snapshots, newest first.",
    )


__all__ = (
    "CalculateTopographyMetricsRequest",
    "TopographyMetricsHistoryResponse",
    "TopographyMetricsResponse",
)
