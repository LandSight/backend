"""Get infrastructure objects use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.infrastructure.application.dto.command import GetInfrastructureObjectsCommand
from app.module.infrastructure.application.dto.response import (
    InfrastructureObjectFeature,
    InfrastructureObjectFeatureCollection,
    InfrastructureObjectProperties,
)
from app.module.infrastructure.application.error import (
    InfrastructureMetricsByIdNotFoundError,
    UnknownCategoryError,
)
from app.module.infrastructure.domain.value_object import Category, InfrastructureMetricsId
from app.module.shared.application.dto.geojson import (
    GeoJSONLineString,
    GeoJSONPoint,
    GeoJSONPolygon,
)
from app.module.shared.application.use_case import BaseUseCase
from app.module.shared.domain.value_object import GeoPoint, LineString, Polygon
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from app.module.infrastructure.application.port import (
        BufferService,
        InfrastructureMetricsService,
        LocalInfrastructureRepository,
        MetricsRepository,
        ParcelProvider,
    )
    from app.module.infrastructure.domain.entity import (
        EcologyMetrics,
        FacilityMetrics,
        GeographicPositionMetrics,
        InfrastructureMetrics,
        InfrastructureObject,
        RoadAccessibilityMetrics,
        UtilityMetrics,
    )
    from app.module.infrastructure.domain.value_object import BufferZone

    _SnapshotLoader = Callable[[Category, InfrastructureMetricsId], Awaitable[InfrastructureMetrics | None]]
    _ObjectLoader = Callable[[BufferZone, Category], Awaitable[list[InfrastructureObject]]]


class GetInfrastructureObjectsUseCase(
    BaseUseCase[GetInfrastructureObjectsCommand, InfrastructureObjectFeatureCollection],
):
    """Retrieve the objects a metrics snapshot was computed over.

    The buffer and parcel are taken from the snapshot itself, so the returned
    objects match the spatial scope used for the metric.
    """

    def __init__(
        self,
        buffer_service: BufferService,
        local_infrastructure_repository: LocalInfrastructureRepository,
        infrastructure_metrics_service: InfrastructureMetricsService,
        metrics_repository: MetricsRepository,
        parcel_provider: ParcelProvider,
    ) -> None:
        self._buffer_service = buffer_service
        self._local_infrastructure_repository = local_infrastructure_repository
        self._infrastructure_metrics_service = infrastructure_metrics_service
        self._metrics_repository = metrics_repository
        self._parcel_provider = parcel_provider
        self._logger = get_logger("app.infrastructure.use_case.get_infrastructure_objects")

        facility = self._load_facility
        ecology = self._load_ecology
        utility = self._load_utility
        self._snapshot_handlers: dict[Category, _SnapshotLoader] = {
            Category.HOSPITAL: facility,
            Category.GROCERY: facility,
            Category.BUS_STOP: facility,
            Category.RAILWAY_STATION: facility,
            Category.POLICE: facility,
            Category.FIRE_STATION: facility,
            Category.PHARMACY: facility,
            Category.WATER_SOURCE: facility,
            Category.WATER_BODY: ecology,
            Category.FOREST: ecology,
            Category.PROTECTED_AREA: ecology,
            Category.POWER_LINE: utility,
            Category.ROAD_ACCESSIBILITY: self._load_road_accessibility,
            Category.GEOGRAPHIC_POSITION: self._load_geographic_position,
        }

        facility = self._facility_objects
        point = self._point_objects
        line = self._line_objects
        polygon = self._polygon_objects
        self._object_handlers: dict[Category, _ObjectLoader] = {
            Category.HOSPITAL: facility,
            Category.GROCERY: facility,
            Category.BUS_STOP: facility,
            Category.RAILWAY_STATION: facility,
            Category.POLICE: facility,
            Category.FIRE_STATION: facility,
            Category.PHARMACY: facility,
            Category.WATER_SOURCE: facility,
            Category.GEOGRAPHIC_POSITION: point,
            Category.WATER_BODY: self._water_body_objects,
            Category.FOREST: polygon,
            Category.PROTECTED_AREA: polygon,
            Category.POWER_LINE: line,
            Category.ROAD_ACCESSIBILITY: line,
        }

    @override
    async def __call__(self, command: GetInfrastructureObjectsCommand) -> InfrastructureObjectFeatureCollection:
        category = self._parse_category(command.category)
        metrics_id = InfrastructureMetricsId(command.metrics_id)

        self._logger.info(
            "Getting infrastructure objects: category=%s metrics_id=%s",
            category.value,
            command.metrics_id,
        )

        snapshot = await self._snapshot_handlers[category](category, metrics_id)
        if snapshot is None:
            raise InfrastructureMetricsByIdNotFoundError(str(command.metrics_id))

        # The Parcel module returns the geometry only for authorized users,
        # so this doubles as the access control gate.
        geo_polygon = await self._parcel_provider.get_parcel_polygon(
            snapshot.parcel_id.unwrap(),
            command.current_user_id,
        )
        polygon = Polygon(
            tuple(GeoPoint.create(float(coord[1]), float(coord[0])) for coord in geo_polygon.coordinates[0])
        )
        zone = self._buffer_service.create_zone(polygon, snapshot.buffer)

        objects = await self._object_handlers[category](zone, category)
        features = [
            InfrastructureObjectFeature(
                geometry=self._to_geometry(obj.geometry),
                properties=InfrastructureObjectProperties(
                    osm_id=obj.id.unwrap(),
                    name=obj.name,
                    category=category.value,
                ),
            )
            for obj in objects
        ]

        return InfrastructureObjectFeatureCollection(features=features)

    @staticmethod
    def _parse_category(category: str) -> Category:
        """Parse a category string, raising a 400-mapped error if unknown."""
        try:
            return Category(category)
        except ValueError as exc:
            raise UnknownCategoryError(category) from exc

    async def _load_facility(
        self,
        category: Category,
        metrics_id: InfrastructureMetricsId,
    ) -> FacilityMetrics | None:
        """Load a facility snapshot, rejecting a category that does not match its type."""
        snapshot = await self._metrics_repository.get_facility_by_id(metrics_id)
        if snapshot is None or snapshot.facility_type is not category:
            return None
        return snapshot

    async def _load_ecology(
        self,
        category: Category,
        metrics_id: InfrastructureMetricsId,
    ) -> EcologyMetrics | None:
        """Load an ecology snapshot, rejecting a category that does not match its type."""
        snapshot = await self._metrics_repository.get_ecology_by_id(metrics_id)
        if snapshot is None or snapshot.object_type is not category:
            return None
        return snapshot

    async def _load_utility(
        self,
        category: Category,
        metrics_id: InfrastructureMetricsId,
    ) -> UtilityMetrics | None:
        """Load a utility snapshot, rejecting a category that does not match its type."""
        snapshot = await self._metrics_repository.get_utility_by_id(metrics_id)
        if snapshot is None or snapshot.utility_type is not category:
            return None
        return snapshot

    async def _load_road_accessibility(
        self,
        category: Category,  # noqa: ARG002
        metrics_id: InfrastructureMetricsId,
    ) -> RoadAccessibilityMetrics | None:
        """Load a road accessibility snapshot."""
        return await self._metrics_repository.get_road_accessibility_by_id(metrics_id)

    async def _load_geographic_position(
        self,
        category: Category,  # noqa: ARG002
        metrics_id: InfrastructureMetricsId,
    ) -> GeographicPositionMetrics | None:
        """Load a geographic position snapshot."""
        return await self._metrics_repository.get_geographic_position_by_id(metrics_id)

    async def _facility_objects(
        self,
        zone: BufferZone,
        category: Category,
    ) -> list[InfrastructureObject]:
        """Read facility objects from both layers, reducing areas to a point.

        Schools, hospitals, shops and stops may be mapped as nodes or as areas;
        areas are turned into their representative point so the map and the
        metrics use a single location per object.
        """
        points = await self._local_infrastructure_repository.get_point_objects(zone, category)
        polygons = await self._local_infrastructure_repository.get_polygon_objects(zone, category)
        return self._infrastructure_metrics_service.to_point_objects([*points, *polygons])

    async def _point_objects(
        self,
        zone: BufferZone,
        category: Category,
    ) -> list[InfrastructureObject]:
        """Read point objects of a category."""
        return await self._local_infrastructure_repository.get_point_objects(zone, category)

    async def _line_objects(
        self,
        zone: BufferZone,
        category: Category,
    ) -> list[InfrastructureObject]:
        """Read line objects of a category."""
        return await self._local_infrastructure_repository.get_line_objects(zone, category)

    async def _polygon_objects(
        self,
        zone: BufferZone,
        category: Category,
    ) -> list[InfrastructureObject]:
        """Read polygon objects of a category."""
        return await self._local_infrastructure_repository.get_polygon_objects(zone, category)

    async def _water_body_objects(
        self,
        zone: BufferZone,
        category: Category,
    ) -> list[InfrastructureObject]:
        """Read water bodies from both the polygon and the river line layer."""
        polygons = await self._local_infrastructure_repository.get_polygon_objects(zone, category)
        rivers = await self._local_infrastructure_repository.get_line_objects(zone, category)
        return [*polygons, *rivers]

    @staticmethod
    def _to_geometry(geometry: GeoPoint | LineString | Polygon) -> GeoJSONPoint | GeoJSONLineString | GeoJSONPolygon:
        """Convert a domain geometry to a GeoJSON geometry DTO."""
        match geometry:
            case GeoPoint():
                return GeoJSONPoint(coordinates=[geometry.longitude.unwrap(), geometry.latitude.unwrap()])
            case LineString():
                return GeoJSONLineString(
                    coordinates=[[point.longitude.unwrap(), point.latitude.unwrap()] for point in geometry.points],
                )
            case Polygon():
                return GeoJSONPolygon(
                    coordinates=[
                        [[point.longitude.unwrap(), point.latitude.unwrap()] for point in geometry.points],
                    ],
                )
            case _:
                message = f"Unsupported geometry type: {type(geometry).__name__}."
                raise TypeError(message)


__all__ = ("GetInfrastructureObjectsUseCase",)
