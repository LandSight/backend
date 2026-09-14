"""Topography HTTP schemas (Pydantic)."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class CalculateTopographyMetricsRequest(BaseModel):
    """Request body for calculating topography metrics."""

    parcel_id: UUID = Field(
        description="ID of the parcel to calculate metrics for.",
    )


__all__ = ("CalculateTopographyMetricsRequest",)
