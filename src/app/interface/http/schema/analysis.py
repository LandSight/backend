"""Analysis HTTP schemas (Pydantic)."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from app.interface.http.schema.climate import ClimateMetricsResponse
from app.interface.http.schema.infrastructure import InfrastructureMetricsResponse
from app.interface.http.schema.topography import TopographyMetricsResponse


class ParcelAnalysisResponse(BaseModel):
    """Response body for the aggregated analysis of a parcel."""

    parcel_id: UUID = Field(description="ID of the parcel.")
    topography: TopographyMetricsResponse = Field(
        description="Topography metrics.",
    )
    infrastructure: InfrastructureMetricsResponse = Field(
        description="Infrastructure metrics (per category).",
    )
    climate: ClimateMetricsResponse = Field(
        description="Climate metrics.",
    )


__all__ = ("ParcelAnalysisResponse",)
