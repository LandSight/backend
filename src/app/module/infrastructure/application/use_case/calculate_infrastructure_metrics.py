"""Calculate infrastructure metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, override
from uuid import uuid6

from app.module.infrastructure.application.dto.command import (
    CalculateInfrastructureMetricsCommand,
    CategoryRequest,
)
from app.module.infrastructure.application.dto.response import (
    CategoryMetricsResponse,
    InfrastructureMetricsResponse,
)
from app.module.infrastructure.domain.entity import (
    HospitalMetrics,
    SchoolMetrics,
    ShopMetrics,
    TransitStopMetrics,
)
from app.module.infrastructure.domain.value_object import (
    Buffer,
    Category,
    Count,
    Distance,
    InfrastructureMetricsId,
    ParcelId,
)
from app.module.shared.application.use_case import BaseUseCase
from app.module.shared.domain.value_object import GeoPoint, Polygon
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from app.module.infrastructure.application.port import (
        BufferService,
        InfrastructureMetricsService,
        LocalInfrastructureRepository,
        MetricsRepository,
    )
    from app.module.infrastructure.domain.entity import InfrastructureObject


class CalculateInfrastructureMetricsUseCase(
    BaseUseCase[CalculateInfrastructureMetricsCommand, InfrastructureMetricsResponse]
):
    """Calculate infrastructure metrics for a parcel.

    For each requested category, builds the buffer zone, fetches raw objects
    from the local data source, computes the metrics, persists them, and
    aggregates the results into a single response.

    When no categories are requested, a default set of categories with default
    buffer radii is used.
    """

    _DEFAULT_CATEGORIES: ClassVar[dict[Category, int]] = {
        Category.SCHOOL: 1000,
        Category.HOSPITAL: 2000,
        Category.SHOP: 500,
        Category.TRANSIT_STOP: 500,
    }

    def __init__(
        self,
        buffer_service: BufferService,
        local_infrastructure_repository: LocalInfrastructureRepository,
        infrastructure_metrics_service: InfrastructureMetricsService,
        metrics_repository: MetricsRepository,
    ) -> None:
        self._buffer_service = buffer_service
        self._local_infrastructure_repository = local_infrastructure_repository
        self._infrastructure_metrics_service = infrastructure_metrics_service
        self._metrics_repository = metrics_repository
        self._logger = get_logger("app.infrastructure.use_case.calculate_infrastructure_metrics")

        self._handlers: dict[
            Category,
            Callable[
                [InfrastructureMetricsId, ParcelId, Buffer, list[InfrastructureObject], Polygon],
                Awaitable[CategoryMetricsResponse],
            ],
        ] = {
            Category.SCHOOL: self._handle_schools,
            Category.HOSPITAL: self._handle_hospitals,
            Category.SHOP: self._handle_shops,
            Category.TRANSIT_STOP: self._handle_transit_stops,
        }

    @override
    async def __call__(self, command: CalculateInfrastructureMetricsCommand) -> InfrastructureMetricsResponse:
        self._logger.info("Calculating infrastructure metrics: parcel_id=%s", command.parcel_id)

        parcel_id = ParcelId(command.parcel_id)
        polygon = Polygon(
            tuple(GeoPoint.create(float(coord[1]), float(coord[0])) for coord in command.polygon["coordinates"][0])
        )

        results: dict[Category, CategoryMetricsResponse] = {}

        category_requests = command.categories or [
            CategoryRequest(category=category.value, buffer=buffer)
            for category, buffer in self._DEFAULT_CATEGORIES.items()
        ]

        for category_request in category_requests:
            category = Category(category_request.category)
            buffer = Buffer(category_request.buffer)
            zone = self._buffer_service.create_zone(polygon, buffer)
            objects = await self._local_infrastructure_repository.get_objects(zone, category)
            result = await self._handlers[category](
                InfrastructureMetricsId(uuid6()),
                parcel_id,
                buffer,
                objects,
                polygon,
            )
            results[category] = result

        self._logger.info(
            "Infrastructure metrics calculated: parcel_id=%s categories=%s",
            command.parcel_id,
            list(results),
        )

        return InfrastructureMetricsResponse(
            parcel_id=command.parcel_id,
            **{category.value: result for category, result in results.items()},
        )

    async def _handle_schools(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        objects: list[InfrastructureObject],
        polygon: Polygon,
    ) -> CategoryMetricsResponse:
        result = self._infrastructure_metrics_service.calculate_schools(objects, polygon)
        metrics = SchoolMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            count=Count(result.count),
            min_distance_to=Distance(result.min_distance_to) if result.min_distance_to is not None else None,
        )
        await self._metrics_repository.save_schools(metrics)
        return result

    async def _handle_hospitals(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        objects: list[InfrastructureObject],
        polygon: Polygon,
    ) -> CategoryMetricsResponse:
        result = self._infrastructure_metrics_service.calculate_hospitals(objects, polygon)
        metrics = HospitalMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            count=Count(result.count),
            min_distance_to=Distance(result.min_distance_to) if result.min_distance_to is not None else None,
        )
        await self._metrics_repository.save_hospitals(metrics)
        return result

    async def _handle_shops(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        objects: list[InfrastructureObject],
        polygon: Polygon,
    ) -> CategoryMetricsResponse:
        result = self._infrastructure_metrics_service.calculate_shops(objects, polygon)
        metrics = ShopMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            count=Count(result.count),
            min_distance_to=Distance(result.min_distance_to) if result.min_distance_to is not None else None,
        )
        await self._metrics_repository.save_shops(metrics)
        return result

    async def _handle_transit_stops(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        objects: list[InfrastructureObject],
        polygon: Polygon,
    ) -> CategoryMetricsResponse:
        result = self._infrastructure_metrics_service.calculate_transit_stops(objects, polygon)
        metrics = TransitStopMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            count=Count(result.count),
            min_distance_to=Distance(result.min_distance_to) if result.min_distance_to is not None else None,
        )
        await self._metrics_repository.save_transit_stops(metrics)
        return result


__all__ = ("CalculateInfrastructureMetricsUseCase",)
