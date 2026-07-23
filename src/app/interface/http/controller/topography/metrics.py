"""Topography metrics HTTP endpoints."""

from __future__ import annotations

from uuid import UUID

from litestar import get, post
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.schema.topography import (
    CalculateTopographyMetricsRequest,
    TopographyMetricsResponse as TopographyMetricsSchema,
)
from app.interface.http.util.guards import require_authorization
from app.module.shared.interface.internal.geojson import GeoJSONPolygon
from app.module.topography.interface.internal.dto import (
    CalculateMetricsInput,
    GetMetricsInput,
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
        current_user: CurrentUser,  # noqa: ARG002
    ) -> TopographyMetricsSchema:
        """Calculate topography metrics for a parcel."""
        result = await topography_api.calculate_metrics(
            CalculateMetricsInput(
                parcel_id=data.parcel_id,
                polygon=GeoJSONPolygon(
                    type=data.polygon.type,
                    coordinates=data.polygon.coordinates,
                ),
            )
        )
        return TopographyMetricsSchema(
            id=result.id,
            parcel_id=result.parcel_id,
            mean_elevation=result.mean_elevation,
            max_elevation=result.max_elevation,
            min_elevation=result.min_elevation,
            elevation_range=result.elevation_range,
            elevation_std=result.elevation_std,
            mean_slope=result.mean_slope,
            max_slope=result.max_slope,
            slope_percentiles=result.slope_percentiles,
            slope_distribution=result.slope_distribution,
            aspect=result.aspect,
            south_aspect_percentage=result.south_aspect_percentage,
            area=result.area,
            perimeter=result.perimeter,
            compactness_index=result.compactness_index,
            elongation_index=result.elongation_index,
        )

    @get(
        "/{parcel_id:uuid}",
        status_code=HTTP_200_OK,
        description="Get topography metrics for a parcel.",
    )
    async def get_topography_metrics(
        self,
        parcel_id: UUID,
        topography_api: TopographyInternalAPI,
        current_user: CurrentUser,  # noqa: ARG002
    ) -> TopographyMetricsSchema:
        """Get topography metrics for a parcel by its ID."""
        result = await topography_api.get_metrics(
            GetMetricsInput(parcel_id=parcel_id),
        )
        return TopographyMetricsSchema(
            id=result.id,
            parcel_id=result.parcel_id,
            mean_elevation=result.mean_elevation,
            max_elevation=result.max_elevation,
            min_elevation=result.min_elevation,
            elevation_range=result.elevation_range,
            elevation_std=result.elevation_std,
            mean_slope=result.mean_slope,
            max_slope=result.max_slope,
            slope_percentiles=result.slope_percentiles,
            slope_distribution=result.slope_distribution,
            aspect=result.aspect,
            south_aspect_percentage=result.south_aspect_percentage,
            area=result.area,
            perimeter=result.perimeter,
            compactness_index=result.compactness_index,
            elongation_index=result.elongation_index,
        )


__all__ = ("TopographyMetricsController",)
