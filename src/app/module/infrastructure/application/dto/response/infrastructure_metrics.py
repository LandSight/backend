"""Infrastructure metrics response DTO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.infrastructure.application.dto.response.category_metrics_response import CategoryMetricsResponse
    from app.module.infrastructure.application.dto.response.water_body_metrics_response import WaterBodyMetricsResponse


@dataclass(frozen=True, slots=True)
class InfrastructureMetricsResponse:
    """Response DTO for infrastructure metrics.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel these metrics belong to.
    school : CategoryMetricsResponse | None
        School metrics, or ``None`` if not requested.
    hospital : CategoryMetricsResponse | None
        Hospital metrics, or ``None`` if not requested.
    shop : CategoryMetricsResponse | None
        Shop metrics, or ``None`` if not requested.
    transit_stop : CategoryMetricsResponse | None
        Transit stop metrics, or ``None`` if not requested.
    water_body : WaterBodyMetricsResponse | None
        Water body metrics, or ``None`` if not requested.
    """

    parcel_id: UUID
    school: CategoryMetricsResponse | None = None
    hospital: CategoryMetricsResponse | None = None
    shop: CategoryMetricsResponse | None = None
    transit_stop: CategoryMetricsResponse | None = None
    water_body: WaterBodyMetricsResponse | None = None


__all__ = ("InfrastructureMetricsResponse",)
