"""Climate HTTP schemas (Pydantic)."""

from __future__ import annotations

import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CalculateClimateMetricsRequest(BaseModel):
    """Request body for calculating climate metrics."""

    parcel_id: UUID = Field(
        description="ID of the parcel to calculate metrics for.",
    )


class ClimateMetricsResponse(BaseModel):
    """Response body for climate metrics."""

    id: UUID = Field(description="Climate metrics identifier.")
    parcel_id: UUID = Field(description="ID of the parcel these metrics belong to.")
    created_at: datetime.datetime | None = Field(description="When these metrics were created (UTC).")
    mean_annual_temperature: float = Field(description="Mean annual temperature (BIO1) in °C.")
    annual_precipitation: float = Field(description="Annual precipitation (BIO12) in mm.")
    temperature_seasonality: float = Field(description="Temperature seasonality (BIO4) in °C.")
    precipitation_seasonality: float = Field(
        description="Precipitation seasonality (BIO15), coefficient of variation in %."
    )
    max_temperature_warmest_month: float = Field(description="Max temperature of the warmest month (BIO5) in °C.")
    min_temperature_coldest_month: float = Field(description="Min temperature of the coldest month (BIO6) in °C.")
    precipitation_wettest_month: float = Field(description="Precipitation of the wettest month (BIO13) in mm.")
    precipitation_driest_month: float = Field(description="Precipitation of the driest month (BIO14) in mm.")


__all__ = (
    "CalculateClimateMetricsRequest",
    "ClimateMetricsResponse",
)
