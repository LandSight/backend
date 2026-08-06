"""Get infrastructure metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, override

from app.module.infrastructure.application.dto.command import (
    CategoryRequest,
    GetInfrastructureMetricsCommand,
)
from app.module.infrastructure.application.dto.response import (
    HospitalMetricsResponse,
    InfrastructureMetricsResponse,
    SchoolMetricsResponse,
    ShopMetricsResponse,
    TransitStopMetricsResponse,
    WaterBodyMetricsResponse,
)
from app.module.infrastructure.domain.value_object import Buffer, Category, ParcelId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from app.module.infrastructure.application.port import MetricsRepository


class GetInfrastructureMetricsUseCase(BaseUseCase[GetInfrastructureMetricsCommand, InfrastructureMetricsResponse]):
    """Get infrastructure metrics for a parcel.

    Retrieves metrics for requested categories with specified buffers.
    If a category has no metrics, the corresponding field is None.

    When no categories are requested, a default set of categories with default
    buffer radii is used.
    """

    _DEFAULT_CATEGORY_BUFFER: ClassVar[dict[Category, int]] = {
        Category.SCHOOL: 1000,
        Category.HOSPITAL: 2000,
        Category.SHOP: 500,
        Category.TRANSIT_STOP: 500,
        Category.WATER_BODY: 1000,
    }

    def __init__(self, metrics_repository: MetricsRepository) -> None:
        self._metrics_repository = metrics_repository
        self._logger = get_logger("app.infrastructure.use_case.get_infrastructure_metrics")

        self._handlers: dict[
            Category,
            Callable[[ParcelId, Buffer], Awaitable[Any]],
        ] = {
            Category.SCHOOL: self._handle_schools,
            Category.HOSPITAL: self._handle_hospitals,
            Category.SHOP: self._handle_shops,
            Category.TRANSIT_STOP: self._handle_transit_stops,
            Category.WATER_BODY: self._handle_water_bodies,
        }

    @override
    async def __call__(self, command: GetInfrastructureMetricsCommand) -> InfrastructureMetricsResponse:
        self._logger.info("Getting infrastructure metrics: parcel_id=%s", command.parcel_id)

        parcel_id = ParcelId(command.parcel_id)

        category_requests = command.categories or [
            CategoryRequest(category=category.value, buffer=buffer)
            for category, buffer in self._DEFAULT_CATEGORY_BUFFER.items()
        ]

        results: dict[Category, Any] = {}

        for category_request in category_requests:
            category = Category(category_request.category)
            buffer = Buffer(category_request.buffer)

            result = await self._handlers[category](parcel_id, buffer)
            results[category] = result

        self._logger.info(
            "Metrics retrieved: parcel_id=%s categories=%s",
            command.parcel_id,
            list(results),
        )

        return InfrastructureMetricsResponse(
            parcel_id=command.parcel_id,
            school=results.get(Category.SCHOOL),
            hospital=results.get(Category.HOSPITAL),
            shop=results.get(Category.SHOP),
            transit_stop=results.get(Category.TRANSIT_STOP),
            water_body=results.get(Category.WATER_BODY),
        )

    async def _handle_schools(self, parcel_id: ParcelId, buffer: Buffer) -> SchoolMetricsResponse | None:
        """Retrieve school metrics for a parcel and buffer."""
        entity = await self._metrics_repository.get_schools(parcel_id, buffer)
        if entity is None:
            return None

        return SchoolMetricsResponse(
            buffer=entity.buffer.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
        )

    async def _handle_hospitals(self, parcel_id: ParcelId, buffer: Buffer) -> HospitalMetricsResponse | None:
        """Retrieve hospital metrics for a parcel and buffer."""
        entity = await self._metrics_repository.get_hospitals(parcel_id, buffer)
        if entity is None:
            return None

        return HospitalMetricsResponse(
            buffer=entity.buffer.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
        )

    async def _handle_shops(self, parcel_id: ParcelId, buffer: Buffer) -> ShopMetricsResponse | None:
        """Retrieve shop metrics for a parcel and buffer."""
        entity = await self._metrics_repository.get_shops(parcel_id, buffer)
        if entity is None:
            return None

        return ShopMetricsResponse(
            buffer=entity.buffer.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
        )

    async def _handle_transit_stops(self, parcel_id: ParcelId, buffer: Buffer) -> TransitStopMetricsResponse | None:
        """Retrieve transit stop metrics for a parcel and buffer."""
        entity = await self._metrics_repository.get_transit_stops(parcel_id, buffer)
        if entity is None:
            return None

        return TransitStopMetricsResponse(
            buffer=entity.buffer.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
        )

    async def _handle_water_bodies(self, parcel_id: ParcelId, buffer: Buffer) -> WaterBodyMetricsResponse | None:
        """Retrieve water body metrics for a parcel and buffer."""
        entity = await self._metrics_repository.get_water_bodies(parcel_id, buffer)
        if entity is None:
            return None

        return WaterBodyMetricsResponse(
            buffer=entity.buffer.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
            coverage_ratio=entity.coverage_ratio.unwrap(),
        )


__all__ = ("GetInfrastructureMetricsUseCase",)
