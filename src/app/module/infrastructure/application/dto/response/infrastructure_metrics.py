"""Infrastructure metrics response DTO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.infrastructure.application.dto.response.category_metrics import (
        HospitalMetricsResponse,
        SchoolMetricsResponse,
        ShopMetricsResponse,
        TransitStopMetricsResponse,
        WaterBodyMetricsResponse,
    )


@dataclass(frozen=True, slots=True)
class InfrastructureMetricsResponse:
    """Response DTO for infrastructure metrics.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel these metrics belong to.
    school : SchoolMetricsResponse | None
        School metrics, or ``None`` if not requested.
    hospital : HospitalMetricsResponse | None
        Hospital metrics, or ``None`` if not requested.
    shop : ShopMetricsResponse | None
        Shop metrics, or ``None`` if not requested.
    transit_stop : TransitStopMetricsResponse | None
        Transit stop metrics, or ``None`` if not requested.
    water_body : WaterBodyMetricsResponse | None
        Water body metrics, or ``None`` if not requested.
    """

    parcel_id: UUID
    school: SchoolMetricsResponse | None = None
    hospital: HospitalMetricsResponse | None = None
    shop: ShopMetricsResponse | None = None
    transit_stop: TransitStopMetricsResponse | None = None
    water_body: WaterBodyMetricsResponse | None = None


__all__ = ("InfrastructureMetricsResponse",)
