"""Concrete implementation of the Topography module's internal API.

See :class:`app.module.topography.interface.internal.port.TopographyInternalAPI`
for the abstract interface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.topography.application.dto.command import (
    CalculateTopographyMetricsCommand,
    GetTopographyMetricsCommand,
)
from app.module.topography.interface.internal.dto import (
    CalculateMetricsInput,
    GetMetricsInput,
    TopographyMetricsResult,
)
from app.module.topography.interface.internal.port import TopographyInternalAPI


if TYPE_CHECKING:
    from app.module.topography.application.use_case import (
        CalculateTopographyMetricsUseCase,
        GetTopographyMetricsUseCase,
    )


class TopographyInternal(TopographyInternalAPI):
    """Concrete implementation of the Topography internal API.

    Wraps the application-layer use cases into a single cohesive
    interface that the HTTP layer calls.
    """

    def __init__(
        self,
        calculate_use_case: CalculateTopographyMetricsUseCase,
        get_use_case: GetTopographyMetricsUseCase,
    ) -> None:
        self._calculate = calculate_use_case
        self._get = get_use_case

    @override
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> TopographyMetricsResult:
        """See :meth:`TopographyInternalAPI.calculate_metrics`."""
        result = await self._calculate(
            CalculateTopographyMetricsCommand(
                parcel_id=input_data.parcel_id,
                polygon={
                    "type": input_data.polygon.type,
                    "coordinates": input_data.polygon.coordinates,
                },
            )
        )
        return TopographyMetricsResult(
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

    @override
    async def get_metrics(self, input_data: GetMetricsInput) -> TopographyMetricsResult:
        """See :meth:`TopographyInternalAPI.get_metrics`."""
        result = await self._get(
            GetTopographyMetricsCommand(
                parcel_id=input_data.parcel_id,
            )
        )
        return TopographyMetricsResult(
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


__all__ = ("TopographyInternal",)
