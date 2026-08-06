"""Concrete implementation of the Infrastructure module's internal API.

See :class:`app.module.infrastructure.interface.internal.port.InfrastructureInternalAPI`
for the abstract interface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.infrastructure.application.dto.command import (
    CalculateInfrastructureMetricsCommand,
    CategoryRequest,
    GetInfrastructureMetricsCommand,
)
from app.module.infrastructure.interface.internal.dto import (
    CalculateMetricsInput,
    CategoryInfoResult,
    GetMetricsInput,
    HospitalMetricsResult,
    InfrastructureMetricsResult,
    SchoolMetricsResult,
    ShopMetricsResult,
    TransitStopMetricsResult,
    WaterBodyMetricsResult,
)
from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI


if TYPE_CHECKING:
    from app.module.infrastructure.application.dto.response import (
        HospitalMetricsResponse,
        InfrastructureMetricsResponse,
        SchoolMetricsResponse,
        ShopMetricsResponse,
        TransitStopMetricsResponse,
        WaterBodyMetricsResponse,
    )
    from app.module.infrastructure.application.use_case import (
        CalculateInfrastructureMetricsUseCase,
        GetAvailableCategoriesUseCase,
        GetInfrastructureMetricsUseCase,
    )


class InfrastructureInternal(InfrastructureInternalAPI):
    """Concrete implementation of the Infrastructure internal API.

    Wraps the application-layer use cases into a single cohesive
    interface that the HTTP layer calls.
    """

    def __init__(
        self,
        calculate_use_case: CalculateInfrastructureMetricsUseCase,
        get_use_case: GetInfrastructureMetricsUseCase,
        get_categories_use_case: GetAvailableCategoriesUseCase,
    ) -> None:
        self._calculate = calculate_use_case
        self._get = get_use_case
        self._get_categories = get_categories_use_case

    @override
    async def calculate_metrics(self, input_data: CalculateMetricsInput) -> InfrastructureMetricsResult:
        """See :meth:`InfrastructureInternalAPI.calculate_metrics`."""
        result = await self._calculate(
            CalculateInfrastructureMetricsCommand(
                parcel_id=input_data.parcel_id,
                polygon={
                    "type": input_data.polygon.type,
                    "coordinates": input_data.polygon.coordinates,
                },
                categories=[CategoryRequest(c.category, c.buffer) for c in input_data.categories],
            )
        )
        return self._to_result(result)

    @override
    async def get_metrics(self, input_data: GetMetricsInput) -> InfrastructureMetricsResult:
        """See :meth:`InfrastructureInternalAPI.get_metrics`."""
        result = await self._get(
            GetInfrastructureMetricsCommand(
                parcel_id=input_data.parcel_id,
                categories=[CategoryRequest(c.category, c.buffer) for c in input_data.categories],
            )
        )
        return self._to_result(result)

    @override
    async def get_available_categories(self) -> list[CategoryInfoResult]:
        """See :meth:`InfrastructureInternalAPI.get_available_categories`."""
        results = await self._get_categories()
        return [CategoryInfoResult(category=r.category) for r in results]

    @staticmethod
    def _to_result(result: InfrastructureMetricsResponse) -> InfrastructureMetricsResult:
        """Convert an application-layer response into an internal result DTO."""
        return InfrastructureMetricsResult(
            parcel_id=result.parcel_id,
            school=InfrastructureInternal._to_school(result.school),
            hospital=InfrastructureInternal._to_hospital(result.hospital),
            shop=InfrastructureInternal._to_shop(result.shop),
            transit_stop=InfrastructureInternal._to_transit_stop(result.transit_stop),
            water_body=InfrastructureInternal._to_water_body(result.water_body),
        )

    @staticmethod
    def _to_school(result: SchoolMetricsResponse | None) -> SchoolMetricsResult | None:
        """Convert a school metrics response into an internal result DTO."""
        if result is None:
            return None
        return SchoolMetricsResult(
            buffer=result.buffer,
            count=result.count,
            min_distance_to=result.min_distance_to,
        )

    @staticmethod
    def _to_hospital(result: HospitalMetricsResponse | None) -> HospitalMetricsResult | None:
        """Convert a hospital metrics response into an internal result DTO."""
        if result is None:
            return None
        return HospitalMetricsResult(
            buffer=result.buffer,
            count=result.count,
            min_distance_to=result.min_distance_to,
        )

    @staticmethod
    def _to_shop(result: ShopMetricsResponse | None) -> ShopMetricsResult | None:
        """Convert a shop metrics response into an internal result DTO."""
        if result is None:
            return None
        return ShopMetricsResult(
            buffer=result.buffer,
            count=result.count,
            min_distance_to=result.min_distance_to,
        )

    @staticmethod
    def _to_transit_stop(result: TransitStopMetricsResponse | None) -> TransitStopMetricsResult | None:
        """Convert a transit stop metrics response into an internal result DTO."""
        if result is None:
            return None
        return TransitStopMetricsResult(
            buffer=result.buffer,
            count=result.count,
            min_distance_to=result.min_distance_to,
        )

    @staticmethod
    def _to_water_body(result: WaterBodyMetricsResponse | None) -> WaterBodyMetricsResult | None:
        """Convert a water body metrics response into an internal result DTO."""
        if result is None:
            return None
        return WaterBodyMetricsResult(
            buffer=result.buffer,
            count=result.count,
            min_distance_to=result.min_distance_to,
            coverage_ratio=result.coverage_ratio,
        )


__all__ = ("InfrastructureInternal",)
