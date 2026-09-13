"""Infrastructure metrics HTTP endpoints.

Metric responses use the shared neutral metrics response schema, matching the
module's internal API so the transferred shape can be inspected uniformly.
"""

from __future__ import annotations

from litestar import get, post
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.schema.infrastructure import (
    CalculateInfrastructureMetricsRequest,
    CategoryInfoSchema,
    GetInfrastructureMetricsByIdsRequest,
    GetInfrastructureMetricsRequest,
)
from app.interface.http.schema.metric_value import MetricsResponseSchema, metrics_response_to_schema
from app.interface.http.util.guards import require_authorization
from app.module.infrastructure.interface.internal.dto import (
    CalculateMetricsInput,
    CategoryMetricRefInput,
    CategoryRequestInput,
    GetMetricsByIdsInput,
    GetMetricsInput,
)
from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI


class InfrastructureMetricsController(Controller):
    """Infrastructure metrics endpoints."""

    path = "/metrics"
    tags = ("infrastructure",)
    guards = [require_authorization]

    @post(
        "/calculate",
        status_code=HTTP_201_CREATED,
        description="Calculate infrastructure metrics for a parcel.",
    )
    async def calculate_infrastructure_metrics(
        self,
        data: CalculateInfrastructureMetricsRequest,
        infrastructure_api: InfrastructureInternalAPI,
        current_user: CurrentUser,
    ) -> list[MetricsResponseSchema]:
        """Calculate infrastructure metrics for a parcel."""
        responses = await infrastructure_api.calculate_metrics(
            CalculateMetricsInput(
                parcel_id=data.parcel_id,
                current_user_id=current_user.id,
                categories=[CategoryRequestInput(c.category, c.buffer) for c in data.categories],
            )
        )
        return [metrics_response_to_schema(response) for response in responses]

    @post(
        "/",
        status_code=HTTP_200_OK,
        description="Get infrastructure metrics for a parcel.",
    )
    async def get_infrastructure_metrics(
        self,
        data: GetInfrastructureMetricsRequest,
        infrastructure_api: InfrastructureInternalAPI,
        current_user: CurrentUser,
    ) -> list[MetricsResponseSchema]:
        """Get infrastructure metrics for a parcel by its ID."""
        responses = await infrastructure_api.get_metrics(
            GetMetricsInput(
                parcel_id=data.parcel_id,
                current_user_id=current_user.id,
                categories=[CategoryRequestInput(c.category, c.buffer) for c in data.categories],
            )
        )
        return [metrics_response_to_schema(response) for response in responses]

    @post(
        "/by-ids",
        status_code=HTTP_200_OK,
        description="Get specific infrastructure metrics records by their IDs.",
    )
    async def get_infrastructure_metrics_by_ids(
        self,
        data: GetInfrastructureMetricsByIdsRequest,
        infrastructure_api: InfrastructureInternalAPI,
        current_user: CurrentUser,
    ) -> list[MetricsResponseSchema]:
        """Get specific infrastructure metrics records by their IDs."""
        responses = await infrastructure_api.get_metrics_by_ids(
            GetMetricsByIdsInput(
                parcel_id=data.parcel_id,
                current_user_id=current_user.id,
                metrics=[CategoryMetricRefInput(m.category, m.metrics_id) for m in data.metrics],
            )
        )
        return [metrics_response_to_schema(response) for response in responses]

    @get(
        "/categories",
        status_code=HTTP_200_OK,
        description="List all available infrastructure categories.",
    )
    async def get_available_categories(
        self,
        infrastructure_api: InfrastructureInternalAPI,
        current_user: CurrentUser,  # noqa: ARG002
    ) -> list[CategoryInfoSchema]:
        """List all available infrastructure categories."""
        results = await infrastructure_api.get_available_categories()
        return [CategoryInfoSchema(category=r.category) for r in results]


__all__ = ("InfrastructureMetricsController",)
