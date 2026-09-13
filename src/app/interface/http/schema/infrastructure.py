"""Infrastructure HTTP schemas (Pydantic)."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class CategoryRequestSchema(BaseModel):
    """Requested infrastructure category with its own buffer radius."""

    category: str = Field(
        description="Infrastructure category (school, hospital, shop, transit_stop, water_body).",
    )
    buffer: int = Field(
        ge=1,
        le=10000,
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
        description="Infrastructure category (school, hospital, shop, transit_stop, water_body).",
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


__all__ = (
    "CalculateInfrastructureMetricsRequest",
    "CategoryInfoSchema",
    "CategoryMetricRefSchema",
    "CategoryRequestSchema",
    "GetInfrastructureMetricsByIdsRequest",
    "GetInfrastructureMetricsRequest",
)
