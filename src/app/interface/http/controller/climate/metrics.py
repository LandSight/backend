"""Climate metrics HTTP endpoints.

Responses use the shared neutral metrics response schema, matching the module's
internal API so the transferred shape can be inspected uniformly.
"""

from __future__ import annotations

from uuid import UUID

from litestar import get, post
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from app.interface.http.schema.climate import CalculateClimateMetricsRequest
from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.schema.metric_value import MetricsResponseSchema, metrics_response_to_schema
from app.interface.http.util.guards import require_authorization
from app.module.climate.interface.internal.dto import (
    CalculateMetricsInput,
    GetMetricsInput,
    GetParcelMetricsInput,
)
from app.module.climate.interface.internal.port import ClimateInternalAPI


class ClimateMetricsController(Controller):
    """Climate metrics endpoints."""

    path = "/metrics"
    tags = ("climate",)
    guards = [require_authorization]

    @post(
        "/calculate",
        status_code=HTTP_201_CREATED,
        description="Calculate climate metrics for a parcel.",
    )
    async def calculate_climate_metrics(
        self,
        data: CalculateClimateMetricsRequest,
        climate_api: ClimateInternalAPI,
        current_user: CurrentUser,
    ) -> MetricsResponseSchema:
        """Calculate climate metrics for a parcel."""
        response = await climate_api.calculate_metrics(
            CalculateMetricsInput(
                parcel_id=data.parcel_id,
                current_user_id=current_user.id,
            )
        )
        return metrics_response_to_schema(response)

    @get(
        "/{metrics_id:uuid}",
        status_code=HTTP_200_OK,
        description="Get a specific climate metrics snapshot by its ID.",
    )
    async def get_climate_metrics(
        self,
        metrics_id: UUID,
        climate_api: ClimateInternalAPI,
        current_user: CurrentUser,
    ) -> MetricsResponseSchema:
        """Get a specific climate metrics snapshot by its ID."""
        response = await climate_api.get_metrics(
            GetMetricsInput(metrics_id=metrics_id, current_user_id=current_user.id)
        )
        return metrics_response_to_schema(response)

    @get(
        "/parcel/{parcel_id:uuid}",
        status_code=HTTP_200_OK,
        description="Get the climate metrics for a parcel.",
    )
    async def get_parcel_climate_metrics(
        self,
        parcel_id: UUID,
        climate_api: ClimateInternalAPI,
        current_user: CurrentUser,
    ) -> MetricsResponseSchema:
        """Get the climate metrics for a parcel."""
        response = await climate_api.get_parcel_metrics(
            GetParcelMetricsInput(parcel_id=parcel_id, current_user_id=current_user.id),
        )
        return metrics_response_to_schema(response)


__all__ = ("ClimateMetricsController",)
