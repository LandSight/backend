"""Calculate infrastructure metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override
from uuid import uuid6

from app.module.infrastructure.application.dto.command import (
    CalculateInfrastructureMetricsCommand,
)
from app.module.infrastructure.application.dto.response import (
    EcologyMetricsResponse,
    FacilityMetricsResponse,
    GeographicPositionMetricsResponse,
    InfrastructureMetricsResponse,
    RoadAccessibilityMetricsResponse,
    UtilityMetricsResponse,
)
from app.module.infrastructure.application.error import UnknownCategoryError
from app.module.infrastructure.domain.entity import (
    EcologyMetrics,
    FacilityMetrics,
    GeographicPositionMetrics,
    RoadAccessibilityMetrics,
    UtilityMetrics,
)
from app.module.infrastructure.domain.metric_policy import LARGE_OBJECT_MIN_AREA_M2
from app.module.infrastructure.domain.value_object import (
    Buffer,
    BufferZone,
    Category,
    CityTier,
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
        InfrastructureObjectClassifier,
        LocalInfrastructureRepository,
        MetricsRepository,
        ParcelProvider,
    )

    _Handler = Callable[
        [InfrastructureMetricsId, ParcelId, Buffer, BufferZone, Category],
        Awaitable[Any],
    ]


class CalculateInfrastructureMetricsUseCase(
    BaseUseCase[CalculateInfrastructureMetricsCommand, InfrastructureMetricsResponse]
):
    """Calculate infrastructure metrics for a parcel.

    For each requested category, builds the buffer zone, fetches raw objects
    from the local data source, computes the metrics, persists them, and
    aggregates the results into a single response.
    """

    def __init__(  # noqa: PLR0913
        self,
        buffer_service: BufferService,
        local_infrastructure_repository: LocalInfrastructureRepository,
        infrastructure_metrics_service: InfrastructureMetricsService,
        metrics_repository: MetricsRepository,
        parcel_provider: ParcelProvider,
        object_classifier: InfrastructureObjectClassifier,
    ) -> None:
        self._buffer_service = buffer_service
        self._local_infrastructure_repository = local_infrastructure_repository
        self._infrastructure_metrics_service = infrastructure_metrics_service
        self._metrics_repository = metrics_repository
        self._parcel_provider = parcel_provider
        self._object_classifier = object_classifier
        self._logger = get_logger("app.infrastructure.use_case.calculate_infrastructure_metrics")

        facility = self._handle_facility
        ecology = self._handle_ecology
        utility = self._handle_utility
        self._handlers: dict[Category, _Handler] = {
            Category.SCHOOL: facility,
            Category.HOSPITAL: facility,
            Category.GROCERY: facility,
            Category.BUS_STOP: facility,
            Category.RAILWAY_STATION: facility,
            Category.WATER_BODY: ecology,
            Category.FOREST: ecology,
            Category.PROTECTED_AREA: ecology,
            Category.POWER_LINE: utility,
            Category.GAS_PIPELINE: utility,
            Category.WATER_PIPELINE: utility,
            Category.ROAD_ACCESSIBILITY: self._handle_road_accessibility,
            Category.GEOGRAPHIC_POSITION: self._handle_geographic_position,
        }

    @override
    async def __call__(self, command: CalculateInfrastructureMetricsCommand) -> InfrastructureMetricsResponse:
        self._logger.info("Calculating infrastructure metrics: parcel_id=%s", command.parcel_id)

        parcel_id = ParcelId(command.parcel_id)

        # The Parcel module returns the geometry only for authorized users,
        # so this doubles as the access control gate for the calculation.
        geo_polygon = await self._parcel_provider.get_parcel_polygon(
            command.parcel_id,
            command.current_user_id,
        )
        polygon = Polygon(
            tuple(GeoPoint.create(float(coord[1]), float(coord[0])) for coord in geo_polygon.coordinates[0])
        )

        results: dict[str, Any] = {}

        for category_request in command.categories:
            category = self._parse_category(category_request.category)
            buffer = Buffer(category_request.buffer)
            zone = self._buffer_service.create_zone(polygon, buffer)
            result = await self._handlers[category](
                InfrastructureMetricsId(uuid6()),
                parcel_id,
                buffer,
                zone,
                category,
            )
            results[category.value] = result

        self._logger.info(
            "Infrastructure metrics calculated: parcel_id=%s categories=%s",
            command.parcel_id,
            list(results),
        )

        return InfrastructureMetricsResponse(parcel_id=command.parcel_id, categories=results)

    @staticmethod
    def _parse_category(category: str) -> Category:
        """Parse a category string, raising a 400-mapped error if unknown."""
        try:
            return Category(category)
        except ValueError as exc:
            raise UnknownCategoryError(category) from exc

    async def _handle_facility(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        buffer_zone: BufferZone,
        category: Category,
    ) -> FacilityMetricsResponse:
        objects = await self._local_infrastructure_repository.get_point_objects(buffer_zone, category)
        count = self._infrastructure_metrics_service.count_objects(objects)
        min_distance_to = self._infrastructure_metrics_service.min_distance(objects, buffer_zone.inner)

        metrics = FacilityMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            facility_type=category,
            count=count,
            min_distance_to=min_distance_to,
        )
        await self._metrics_repository.save_facility(metrics)
        return FacilityMetricsResponse(
            id=id.unwrap(),
            buffer=buffer.unwrap(),
            count=count.unwrap(),
            min_distance_to=min_distance_to.unwrap() if min_distance_to is not None else None,
        )

    async def _handle_ecology(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        buffer_zone: BufferZone,
        category: Category,
    ) -> EcologyMetricsResponse:
        polygons = await self._local_infrastructure_repository.get_polygon_objects(buffer_zone, category)
        objects = list(polygons)
        if category is Category.WATER_BODY:
            rivers = await self._local_infrastructure_repository.get_line_objects(buffer_zone, category)
            objects.extend(rivers)

        coverage_ratio = self._infrastructure_metrics_service.coverage_ratio(polygons, buffer_zone)
        count = self._infrastructure_metrics_service.count_components(objects)
        min_distance_to = self._infrastructure_metrics_service.min_distance(objects, buffer_zone.inner)

        always_large_ids = frozenset(
            obj.id.unwrap() for obj in objects if self._object_classifier.is_significant_protected_area(obj)
        )
        distance_to_large_object = self._infrastructure_metrics_service.min_distance_to_large_object(
            objects,
            buffer_zone.inner,
            LARGE_OBJECT_MIN_AREA_M2[category],
            always_large_ids,
        )

        metrics = EcologyMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            object_type=category,
            coverage_ratio=coverage_ratio,
            count=count,
            min_distance_to=min_distance_to,
            distance_to_large_object=distance_to_large_object,
        )
        await self._metrics_repository.save_ecology(metrics)
        return EcologyMetricsResponse(
            id=id.unwrap(),
            buffer=buffer.unwrap(),
            coverage_ratio=coverage_ratio.unwrap(),
            count=count.unwrap(),
            min_distance_to=min_distance_to.unwrap() if min_distance_to is not None else None,
            distance_to_large_object=(
                distance_to_large_object.unwrap() if distance_to_large_object is not None else None
            ),
        )

    async def _handle_utility(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        buffer_zone: BufferZone,
        category: Category,
    ) -> UtilityMetricsResponse:
        objects = await self._local_infrastructure_repository.get_line_objects(buffer_zone, category)
        min_distance_to = self._infrastructure_metrics_service.min_distance(objects, buffer_zone.inner)

        metrics = UtilityMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            utility_type=category,
            min_distance_to=min_distance_to,
        )
        await self._metrics_repository.save_utility(metrics)
        return UtilityMetricsResponse(
            id=id.unwrap(),
            buffer=buffer.unwrap(),
            min_distance_to=min_distance_to.unwrap() if min_distance_to is not None else None,
        )

    async def _handle_road_accessibility(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        buffer_zone: BufferZone,
        category: Category,  # noqa: ARG002
    ) -> RoadAccessibilityMetricsResponse:
        roads = await self._local_infrastructure_repository.get_line_objects(buffer_zone, Category.ROAD_ACCESSIBILITY)
        paved_roads = [road for road in roads if self._object_classifier.is_paved_road(road)]

        distance_to_paved_road = self._infrastructure_metrics_service.min_distance(paved_roads, buffer_zone.inner)
        road_density = self._infrastructure_metrics_service.line_density(roads, buffer_zone)

        metrics = RoadAccessibilityMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            distance_to_paved_road=distance_to_paved_road,
            road_density_1km=road_density,
        )
        await self._metrics_repository.save_road_accessibility(metrics)
        return RoadAccessibilityMetricsResponse(
            id=id.unwrap(),
            buffer=buffer.unwrap(),
            distance_to_paved_road=distance_to_paved_road.unwrap() if distance_to_paved_road is not None else None,
            road_density_1km=road_density.unwrap(),
        )

    async def _handle_geographic_position(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
        buffer_zone: BufferZone,
        category: Category,  # noqa: ARG002
    ) -> GeographicPositionMetricsResponse:
        objects = await self._local_infrastructure_repository.get_point_objects(
            buffer_zone, Category.GEOGRAPHIC_POSITION
        )
        nearest = self._infrastructure_metrics_service.nearest_object(objects, buffer_zone.inner)
        if nearest is None:
            distance = None
            tier = CityTier.UNKNOWN
        else:
            distance = self._infrastructure_metrics_service.min_distance([nearest], buffer_zone.inner)
            tier = self._object_classifier.city_tier(nearest)

        metrics = GeographicPositionMetrics(
            id=id,
            parcel_id=parcel_id,
            buffer=buffer,
            distance_to_major_city=distance,
            city_tier=tier,
        )
        await self._metrics_repository.save_geographic_position(metrics)
        return GeographicPositionMetricsResponse(
            id=id.unwrap(),
            buffer=buffer.unwrap(),
            distance_to_major_city=distance.unwrap() if distance is not None else None,
            city_tier=tier.value,
        )


__all__ = ("CalculateInfrastructureMetricsUseCase",)
