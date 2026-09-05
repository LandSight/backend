"""Infrastructure metrics HTTP endpoints."""

from __future__ import annotations

from litestar import get, post
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.schema.infrastructure import (
    CalculateInfrastructureMetricsRequest,
    CategoryInfoSchema,
    GetInfrastructureMetricsRequest,
    HospitalMetricsSchema,
    InfrastructureMetricsResponse,
    SchoolMetricsSchema,
    ShopMetricsSchema,
    TransitStopMetricsSchema,
    WaterBodyMetricsSchema,
)
from app.interface.http.util.guards import require_authorization
from app.module.infrastructure.interface.internal.dto import (
    CalculateMetricsInput,
    CategoryRequestInput,
    GetMetricsInput,
    HospitalMetricsResult,
    InfrastructureMetricsResult,
    SchoolMetricsResult,
    ShopMetricsResult,
    TransitStopMetricsResult,
    WaterBodyMetricsResult,
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
    ) -> InfrastructureMetricsResponse:
        """Calculate infrastructure metrics for a parcel."""
        result = await infrastructure_api.calculate_metrics(
            CalculateMetricsInput(
                parcel_id=data.parcel_id,
                current_user_id=current_user.id,
                categories=[CategoryRequestInput(c.category, c.buffer) for c in data.categories],
            )
        )
        return InfrastructureMetricsController._to_response(result)

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
    ) -> InfrastructureMetricsResponse:
        """Get infrastructure metrics for a parcel by its ID."""
        result = await infrastructure_api.get_metrics(
            GetMetricsInput(
                parcel_id=data.parcel_id,
                current_user_id=current_user.id,
                categories=[CategoryRequestInput(c.category, c.buffer) for c in data.categories],
            )
        )
        return InfrastructureMetricsController._to_response(result)

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

    @staticmethod
    def _to_response(result: InfrastructureMetricsResult) -> InfrastructureMetricsResponse:
        """Convert an internal result into an HTTP response schema."""
        return InfrastructureMetricsResponse(
            parcel_id=result.parcel_id,
            school=InfrastructureMetricsController._to_school(result.school),
            hospital=InfrastructureMetricsController._to_hospital(result.hospital),
            shop=InfrastructureMetricsController._to_shop(result.shop),
            transit_stop=InfrastructureMetricsController._to_transit_stop(result.transit_stop),
            water_body=InfrastructureMetricsController._to_water_body(result.water_body),
        )

    @staticmethod
    def _to_school(result: SchoolMetricsResult | None) -> SchoolMetricsSchema | None:
        """Convert a school metrics result into an HTTP schema."""
        if result is None:
            return None
        return SchoolMetricsSchema(
            buffer=result.buffer,
            count=result.count,
            min_distance_to=result.min_distance_to,
        )

    @staticmethod
    def _to_hospital(result: HospitalMetricsResult | None) -> HospitalMetricsSchema | None:
        """Convert a hospital metrics result into an HTTP schema."""
        if result is None:
            return None
        return HospitalMetricsSchema(
            buffer=result.buffer,
            count=result.count,
            min_distance_to=result.min_distance_to,
        )

    @staticmethod
    def _to_shop(result: ShopMetricsResult | None) -> ShopMetricsSchema | None:
        """Convert a shop metrics result into an HTTP schema."""
        if result is None:
            return None
        return ShopMetricsSchema(
            buffer=result.buffer,
            count=result.count,
            min_distance_to=result.min_distance_to,
        )

    @staticmethod
    def _to_transit_stop(result: TransitStopMetricsResult | None) -> TransitStopMetricsSchema | None:
        """Convert a transit stop metrics result into an HTTP schema."""
        if result is None:
            return None
        return TransitStopMetricsSchema(
            buffer=result.buffer,
            count=result.count,
            min_distance_to=result.min_distance_to,
        )

    @staticmethod
    def _to_water_body(result: WaterBodyMetricsResult | None) -> WaterBodyMetricsSchema | None:
        """Convert a water body metrics result into an HTTP schema."""
        if result is None:
            return None
        return WaterBodyMetricsSchema(
            buffer=result.buffer,
            count=result.count,
            min_distance_to=result.min_distance_to,
            coverage_ratio=result.coverage_ratio,
        )


__all__ = ("InfrastructureMetricsController",)
