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

    parcel_id: UUID = Field(
        description="ID of the parcel to calculate metrics for.",
    )
    categories: list[CategoryRequestSchema] = Field(
        default_factory=list,
        description="Requested categories with their buffer radii.",
    )


class GetInfrastructureMetricsRequest(BaseModel):
    """Request body for retrieving infrastructure metrics."""

    parcel_id: UUID = Field(
        description="ID of the parcel of calculated metrics.",
    )
    categories: list[CategoryRequestSchema] = Field(
        default_factory=list,
        description="Requested categories with their buffer radii.",
    )


class SchoolMetricsSchema(BaseModel):
    """Metrics for the ``school`` category."""

    buffer: int = Field(description="Buffer radius in meters.")
    count: int = Field(description="Number of objects within the buffer zone.")
    min_distance_to: float | None = Field(
        default=None,
        description="Distance to the nearest object in meters, or null if none found.",
    )


class HospitalMetricsSchema(BaseModel):
    """Metrics for the ``hospital`` category."""

    buffer: int = Field(description="Buffer radius in meters.")
    count: int = Field(description="Number of objects within the buffer zone.")
    min_distance_to: float | None = Field(
        default=None,
        description="Distance to the nearest object in meters, or null if none found.",
    )


class ShopMetricsSchema(BaseModel):
    """Metrics for the ``shop`` category."""

    buffer: int = Field(description="Buffer radius in meters.")
    count: int = Field(description="Number of objects within the buffer zone.")
    min_distance_to: float | None = Field(
        default=None,
        description="Distance to the nearest object in meters, or null if none found.",
    )


class TransitStopMetricsSchema(BaseModel):
    """Metrics for the ``transit_stop`` category."""

    buffer: int = Field(description="Buffer radius in meters.")
    count: int = Field(description="Number of objects within the buffer zone.")
    min_distance_to: float | None = Field(
        default=None,
        description="Distance to the nearest object in meters, or null if none found.",
    )


class WaterBodyMetricsSchema(BaseModel):
    """Metrics for the ``water_body`` category."""

    buffer: int = Field(description="Buffer radius in meters.")
    count: int = Field(description="Number of objects within the buffer zone.")
    min_distance_to: float | None = Field(
        default=None,
        description="Distance to the nearest object in meters, or null if none found.",
    )
    coverage_ratio: float = Field(
        description="Coverage ratio of the buffer zone covered by water bodies.",
    )


class InfrastructureMetricsResponse(BaseModel):
    """Response body for infrastructure metrics."""

    parcel_id: UUID = Field(description="ID of the parcel these metrics belong to.")
    school: SchoolMetricsSchema | None = Field(
        default=None,
        description="School metrics, or null if not requested.",
    )
    hospital: HospitalMetricsSchema | None = Field(
        default=None,
        description="Hospital metrics, or null if not requested.",
    )
    shop: ShopMetricsSchema | None = Field(
        default=None,
        description="Shop metrics, or null if not requested.",
    )
    transit_stop: TransitStopMetricsSchema | None = Field(
        default=None,
        description="Transit stop metrics, or null if not requested.",
    )
    water_body: WaterBodyMetricsSchema | None = Field(
        default=None,
        description="Water body metrics, or null if not requested.",
    )


class CategoryInfoSchema(BaseModel):
    """Information about an available infrastructure category."""

    category: str = Field(description="Category identifier.")


__all__ = (
    "CalculateInfrastructureMetricsRequest",
    "CategoryInfoSchema",
    "CategoryRequestSchema",
    "GetInfrastructureMetricsRequest",
    "HospitalMetricsSchema",
    "InfrastructureMetricsResponse",
    "SchoolMetricsSchema",
    "ShopMetricsSchema",
    "TransitStopMetricsSchema",
    "WaterBodyMetricsSchema",
)
