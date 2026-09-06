"""Climate metrics HTTP endpoints."""

from __future__ import annotations

from uuid import UUID

from litestar import get, post
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from app.interface.http.schema.climate import (
    CalculateClimateMetricsRequest,
    ClimateMetricsResponse as ClimateMetricsSchema,
)
from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.util.guards import require_authorization
from app.module.climate.interface.internal.dto import (
    CalculateMetricsInput,
    ClimateMetricsResult,
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
    ) -> ClimateMetricsSchema:
        """Calculate climate metrics for a parcel."""
        result = await climate_api.calculate_metrics(
            CalculateMetricsInput(
                parcel_id=data.parcel_id,
                current_user_id=current_user.id,
            )
        )
        return self._to_schema(result)

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
    ) -> ClimateMetricsSchema:
        """Get a specific climate metrics snapshot by its ID."""
        result = await climate_api.get_metrics(GetMetricsInput(metrics_id=metrics_id, current_user_id=current_user.id))
        return self._to_schema(result)

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
    ) -> ClimateMetricsSchema:
        """Get the climate metrics for a parcel."""
        result = await climate_api.get_parcel_metrics(
            GetParcelMetricsInput(parcel_id=parcel_id, current_user_id=current_user.id),
        )
        return self._to_schema(result)

    @staticmethod
    def _to_schema(result: ClimateMetricsResult) -> ClimateMetricsSchema:
        """Map an internal result DTO to the HTTP response schema."""
        return ClimateMetricsSchema(
            id=result.id,
            parcel_id=result.parcel_id,
            created_at=result.created_at,
            mean_annual_temperature=result.mean_annual_temperature,
            annual_precipitation=result.annual_precipitation,
            temperature_seasonality=result.temperature_seasonality,
            precipitation_seasonality=result.precipitation_seasonality,
            max_temperature_warmest_month=result.max_temperature_warmest_month,
            min_temperature_coldest_month=result.min_temperature_coldest_month,
            precipitation_wettest_month=result.precipitation_wettest_month,
            precipitation_driest_month=result.precipitation_driest_month,
        )


__all__ = ("ClimateMetricsController",)
