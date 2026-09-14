"""Topography metrics HTTP endpoints.

Responses use the shared neutral metrics response schema, matching the module's
internal API so the transferred shape can be inspected uniformly.
"""

from __future__ import annotations

from uuid import UUID

from litestar import get, post
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.schema.metric_value import MetricsResponseSchema, metrics_response_to_schema
from app.interface.http.schema.topography import CalculateTopographyMetricsRequest
from app.interface.http.util.guards import require_authorization
from app.module.topography.interface.internal.dto import (
    CalculateMetricsInput,
    GetMetricsInput,
    GetParcelMetricsInput,
)
from app.module.topography.interface.internal.port import TopographyInternalAPI


class TopographyMetricsController(Controller):
    """Topography metrics endpoints."""

    path = "/metrics"
    tags = ("topography",)
    guards = [require_authorization]

    @post(
        "/calculate",
        status_code=HTTP_201_CREATED,
        description="Calculate topography metrics for a parcel.",
    )
    async def calculate_topography_metrics(
        self,
        data: CalculateTopographyMetricsRequest,
        topography_api: TopographyInternalAPI,
        current_user: CurrentUser,
    ) -> MetricsResponseSchema:
        """Calculate topography metrics for a parcel."""
        response = await topography_api.calculate_metrics(
            CalculateMetricsInput(
                parcel_id=data.parcel_id,
                current_user_id=current_user.id,
            )
        )
        return metrics_response_to_schema(response)

    @get(
        "/{metrics_id:uuid}",
        status_code=HTTP_200_OK,
        description="Get a specific topography metrics snapshot by its ID.",
    )
    async def get_topography_metrics(
        self,
        metrics_id: UUID,
        topography_api: TopographyInternalAPI,
        current_user: CurrentUser,
    ) -> MetricsResponseSchema:
        """Get a specific topography metrics snapshot by its ID."""
        response = await topography_api.get_metrics(
            GetMetricsInput(metrics_id=metrics_id, current_user_id=current_user.id)
        )
        return metrics_response_to_schema(response)

    @get(
        "/parcel/{parcel_id:uuid}",
        status_code=HTTP_200_OK,
        description="Get the topography metrics for a parcel.",
    )
    async def get_parcel_topography_metrics(
        self,
        parcel_id: UUID,
        topography_api: TopographyInternalAPI,
        current_user: CurrentUser,
    ) -> MetricsResponseSchema:
        """Get the topography metrics for a parcel."""
        response = await topography_api.get_parcel_metrics(
            GetParcelMetricsInput(parcel_id=parcel_id, current_user_id=current_user.id),
        )
        return metrics_response_to_schema(response)


__all__ = ("TopographyMetricsController",)
