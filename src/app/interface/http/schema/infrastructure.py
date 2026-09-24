"""Infrastructure HTTP schemas (Pydantic)."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from app.interface.http.schema.geojson import GeoJSONGeometry


class CategoryRequestSchema(BaseModel):
    """Requested infrastructure category with its own buffer radius."""

    category: str = Field(
        description=(
            "Infrastructure category (school, hospital, grocery, bus_stop, railway_station, "
            "water_body, forest, protected_area, power_line, gas_pipeline, water_pipeline, "
            "road_accessibility, geographic_position)."
        ),
    )
    buffer: int = Field(
        ge=1,
        le=200000,
        description="Buffer radius in meters around the parcel boundary.",
    )


class CalculateInfrastructureMetricsRequest(BaseModel):
    """Request body for calculating infrastructure metrics."""

    parcel_id: UUID = Field(description="ID of the parcel to calculate metrics for.")
    categories: list[CategoryRequestSchema] = Field(
        default_factory=list,
        description="Requested categories with their buffer radii.",
    )


class GetInfrastructureMetricsRequest(BaseModel):
    """Request body for retrieving infrastructure metrics."""

    parcel_id: UUID = Field(description="ID of the parcel of calculated metrics.")
    categories: list[CategoryRequestSchema] = Field(
        default_factory=list,
        description="Requested categories with their buffer radii.",
    )


class CategoryMetricRefSchema(BaseModel):
    """Reference to a specific infrastructure metrics record within a category."""

    category: str = Field(
        description=(
            "Infrastructure category (school, hospital, grocery, bus_stop, railway_station, "
            "water_body, forest, protected_area, power_line, gas_pipeline, water_pipeline, "
            "road_accessibility, geographic_position)."
        ),
    )
    metrics_id: UUID = Field(description="ID of the persisted metrics record.")


class GetInfrastructureMetricsByIdsRequest(BaseModel):
    """Request body for retrieving specific infrastructure metrics records by their IDs."""

    parcel_id: UUID = Field(description="ID of the parcel the metrics belong to.")
    metrics: list[CategoryMetricRefSchema] = Field(
        default_factory=list,
        description="Requested (category, metrics_id) references.",
    )


class CategoryInfoSchema(BaseModel):
    """Information about an available infrastructure category."""

    category: str = Field(description="Infrastructure category name.")
    label: str = Field(description="Human-readable category name for the UI.")


class InfrastructureObjectPropertiesSchema(BaseModel):
    """Typed properties of an infrastructure object GeoJSON Feature."""

    osm_id: str = Field(description="OSM identifier of the object.")
    name: str | None = Field(default=None, description="Human-readable name of the object, if any.")
    category: str = Field(description="Infrastructure category the object belongs to.")


class InfrastructureObjectFeatureSchema(BaseModel):
    """GeoJSON Feature of a single infrastructure object."""

    type: str = Field(default="Feature", description='GeoJSON type. Must be ``"Feature"``.')
    geometry: GeoJSONGeometry = Field(description="Object geometry in WGS84 coordinates.")
    properties: InfrastructureObjectPropertiesSchema = Field(description="Object properties.")


class InfrastructureObjectFeatureCollectionSchema(BaseModel):
    """GeoJSON FeatureCollection of the objects behind a metrics snapshot."""

    type: str = Field(
        default="FeatureCollection",
        description='GeoJSON type. Must be ``"FeatureCollection"``.',
    )
    features: list[InfrastructureObjectFeatureSchema] = Field(
        default_factory=list,
        description="GeoJSON features of the objects.",
    )


__all__ = (
    "CalculateInfrastructureMetricsRequest",
    "CategoryInfoSchema",
    "CategoryMetricRefSchema",
    "CategoryRequestSchema",
    "GetInfrastructureMetricsByIdsRequest",
    "GetInfrastructureMetricsRequest",
    "InfrastructureObjectFeatureCollectionSchema",
    "InfrastructureObjectFeatureSchema",
    "InfrastructureObjectPropertiesSchema",
)
