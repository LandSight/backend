"""Calculate infrastructure metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override
from uuid import uuid6

from app.module.infrastructure.application.dto.command import (
    CalculateInfrastructureMetricsCommand,
)
from app.module.infrastructure.application.dto.response import (
    HospitalMetricsResponse,
    InfrastructureMetricsResponse,
    SchoolMetricsResponse,
    ShopMetricsResponse,
    TransitStopMetricsResponse,
    WaterBodyMetricsResponse,
)
from app.module.infrastructure.domain.entity import (
    HospitalMetrics,
    SchoolMetrics,
    ShopMetrics,
    TransitStopMetrics,
    WaterBodyMetrics,
)
from app.module.infrastructure.domain.value_object import (
    Buffer,
    BufferZone,
    Category,
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
                [InfrastructureMetricsId, ParcelId, Buffer, BufferZone],
                Awaitable[Any],
            ],
        ] = {
            Category.SCHOOL: self._handle_schools,
            Category.HOSPITAL: self._handle_hospitals,
            Category.SHOP: self._handle_shops,
            Category.TRANSIT_STOP: self._handle_transit_stops,
            Category.WATER_BODY: self._handle_water_bodies,
        }

    @override
    async def __call__(self, command: CalculateInfrastructureMetricsCommand) -> InfrastructureMetricsResponse:
        self._logger.info("Calculating infrastructure metrics: parcel_id=%s", command.parcel_id)

        parcel_id = ParcelId(command.parcel_id)
        polygon = Polygon(
            tuple(GeoPoint.create(float(coord[1]), float(coord[0])) for coord in command.polygon["coordinates"][0])
        )

        results: dict[Category, Any] = {}

        for category_request in command.categories:
            category = Category(category_request.category)
            buffer = Buffer(category_request.buffer)
            zone = self._buffer_service.create_zone(polygon, buffer)
            result = await self._handlers[category](
                InfrastructureMetricsId(uuid6()),
                parcel_id,
                buffer,
                zone,
            )
            results[category] = result

        self._logger.info(
            "Infrastructure metrics calculated: parcel_id=%s categories=%s",
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

    async def _handle_schools(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        buffer_zone: BufferZone,
    ) -> SchoolMetricsResponse:
        objects = await self._local_infrastructure_repository.get_point_objects(buffer_zone, Category.SCHOOL)
        count = self._infrastructure_metrics_service.count_objects(objects)
        min_distance_to = self._infrastructure_metrics_service.min_distance(objects, buffer_zone.inner)
        metrics = SchoolMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            count=count,
            min_distance_to=min_distance_to,
        )
        await self._metrics_repository.save_schools(metrics)
        response = SchoolMetricsResponse(
            buffer=buffer.unwrap(),
            count=count.unwrap(),
            min_distance_to=min_distance_to.unwrap() if min_distance_to is not None else None,
        )
        return response

    async def _handle_hospitals(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        buffer_zone: BufferZone,
    ) -> HospitalMetricsResponse:
        objects = await self._local_infrastructure_repository.get_point_objects(buffer_zone, Category.HOSPITAL)
        count = self._infrastructure_metrics_service.count_objects(objects)
        min_distance_to = self._infrastructure_metrics_service.min_distance(objects, buffer_zone.inner)
        metrics = HospitalMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            count=count,
            min_distance_to=min_distance_to,
        )
        await self._metrics_repository.save_hospitals(metrics)
        response = HospitalMetricsResponse(
            buffer=buffer.unwrap(),
            count=count.unwrap(),
            min_distance_to=min_distance_to.unwrap() if min_distance_to is not None else None,
        )
        return response

    async def _handle_shops(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        buffer_zone: BufferZone,
    ) -> ShopMetricsResponse:
        objects = await self._local_infrastructure_repository.get_point_objects(buffer_zone, Category.SHOP)
        count = self._infrastructure_metrics_service.count_objects(objects)
        min_distance_to = self._infrastructure_metrics_service.min_distance(objects, buffer_zone.inner)
        metrics = ShopMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            count=count,
            min_distance_to=min_distance_to,
        )
        await self._metrics_repository.save_shops(metrics)
        response = ShopMetricsResponse(
            buffer=buffer.unwrap(),
            count=count.unwrap(),
            min_distance_to=min_distance_to.unwrap() if min_distance_to is not None else None,
        )
        return response

    async def _handle_transit_stops(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        buffer_zone: BufferZone,
    ) -> TransitStopMetricsResponse:
        objects = await self._local_infrastructure_repository.get_point_objects(buffer_zone, Category.TRANSIT_STOP)
        count = self._infrastructure_metrics_service.count_objects(objects)
        min_distance_to = self._infrastructure_metrics_service.min_distance(objects, buffer_zone.inner)
        metrics = TransitStopMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            count=count,
            min_distance_to=min_distance_to,
        )
        await self._metrics_repository.save_transit_stops(metrics)
        response = TransitStopMetricsResponse(
            buffer=buffer.unwrap(),
            count=count.unwrap(),
            min_distance_to=min_distance_to.unwrap() if min_distance_to is not None else None,
        )
        return response

    async def _handle_water_bodies(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        buffer_zone: BufferZone,
    ) -> WaterBodyMetricsResponse:
        objects = await self._local_infrastructure_repository.get_polygon_objects(buffer_zone, Category.WATER_BODY)
        count = self._infrastructure_metrics_service.count_objects(objects)
        min_distance_to = self._infrastructure_metrics_service.min_distance(objects, buffer_zone.inner)
        coverage_ratio = self._infrastructure_metrics_service.coverage_ratio(objects, buffer_zone)
        metrics = WaterBodyMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            count=count,
            min_distance_to=min_distance_to,
            coverage_ratio=coverage_ratio,
        )
        await self._metrics_repository.save_water_bodies(metrics)
        response = WaterBodyMetricsResponse(
            buffer=buffer.unwrap(),
            count=count.unwrap(),
            min_distance_to=min_distance_to.unwrap() if min_distance_to is not None else None,
            coverage_ratio=coverage_ratio.unwrap(),
        )
        return response


__all__ = ("CalculateInfrastructureMetricsUseCase",)
