"""Climate HTTP schemas (Pydantic)."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class CalculateClimateMetricsRequest(BaseModel):
    """Request body for calculating climate metrics."""

    parcel_id: UUID = Field(
        description="ID of the parcel to calculate metrics for.",
    )


__all__ = ("CalculateClimateMetricsRequest",)
