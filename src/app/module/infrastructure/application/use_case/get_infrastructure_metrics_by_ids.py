"""Get infrastructure metrics by IDs use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, override

from app.module.infrastructure.application.dto.command import (
    GetInfrastructureMetricsByIdsCommand,
)
from app.module.infrastructure.application.dto.response import (
    EcologyMetricsResponse,
    FacilityMetricsResponse,
    GeographicPositionMetricsResponse,
    InfrastructureMetricsResponse,
    RoadAccessibilityMetricsResponse,
    UtilityMetricsResponse,
)
from app.module.infrastructure.application.error import (
    InfrastructureMetricsByIdNotFoundError,
    UnknownCategoryError,
)
from app.module.infrastructure.domain.entity import InfrastructureMetrics
from app.module.infrastructure.domain.value_object import (
    Category,
    InfrastructureMetricsId,
    MetricFamily,
    ParcelId,
    family_of,
)
from app.module.shared.application.error import ForbiddenError
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from typing import NoReturn

    from app.module.infrastructure.application.dto.response import CategoryMetricsResponse
    from app.module.infrastructure.application.port import MetricsPermissionService, MetricsRepository

    _Refs = list[tuple[Category, InfrastructureMetricsId]]
    _FamilyHandler = Callable[[_Refs, ParcelId], Awaitable[dict[Category, CategoryMetricsResponse]]]

EntityT = TypeVar("EntityT", bound=InfrastructureMetrics)


class GetInfrastructureMetricsByIdsUseCase(
    BaseUseCase[GetInfrastructureMetricsByIdsCommand, InfrastructureMetricsResponse]
):
    """Retrieve specific infrastructure metrics records by their IDs.

    References are grouped by metrics family and fetched with one query per
    family, so a batch request turns into a small fixed number of queries rather
    than one per reference. All records must belong to the requested parcel;
    access is granted only when the current user owns that parcel.
    """

    def __init__(
        self,
        metrics_repository: MetricsRepository,
        metrics_permission_service: MetricsPermissionService,
    ) -> None:
        self._metrics_repository = metrics_repository
        self._metrics_permission_service = metrics_permission_service
        self._logger = get_logger("app.infrastructure.use_case.get_infrastructure_metrics_by_ids")

        self._family_handlers: dict[MetricFamily, _FamilyHandler] = {
            MetricFamily.FACILITY: self._collect_facility,
            MetricFamily.ECOLOGY: self._collect_ecology,
            MetricFamily.UTILITY: self._collect_utility,
            MetricFamily.ROAD_ACCESSIBILITY: self._collect_road_accessibility,
            MetricFamily.GEOGRAPHIC_POSITION: self._collect_geographic_position,
        }

    @override
    async def __call__(self, command: GetInfrastructureMetricsByIdsCommand) -> InfrastructureMetricsResponse:
        self._logger.info(
            "Getting infrastructure metrics by ids: parcel_id=%s count=%s",
            command.parcel_id,
            len(command.metrics),
        )

        if not await self._metrics_permission_service.user_can_view_parcel_metrics(
            command.current_user_id,
            command.parcel_id,
        ):
            reason = f"User is not allowed to view metrics for parcel '{command.parcel_id}'"
            raise ForbiddenError(reason)

        parcel_id = ParcelId(command.parcel_id)
        grouped: dict[MetricFamily, _Refs] = {}
        for metric in command.metrics:
            category = self._parse_category(metric.category)
            grouped.setdefault(family_of(category), []).append(
                (category, InfrastructureMetricsId(metric.metrics_id)),
            )

        results: dict[Category, CategoryMetricsResponse] = {}
        for family, refs in grouped.items():
            results.update(await self._family_handlers[family](refs, parcel_id))

        return InfrastructureMetricsResponse(
            parcel_id=command.parcel_id,
            categories={category.value: response for category, response in results.items()},
        )

    @staticmethod
    def _parse_category(category: str) -> Category:
        """Parse a category string, raising a 400-mapped error if unknown."""
        try:
            return Category(category)
        except ValueError as exc:
            raise UnknownCategoryError(category) from exc

    async def _collect_facility(
        self,
        refs: _Refs,
        parcel_id: ParcelId,
    ) -> dict[Category, CategoryMetricsResponse]:
        """Fetch and map all referenced facility records in one query."""
        entities = {
            entity.id: entity
            for entity in await self._metrics_repository.get_facilities_by_ids(
                [metrics_id for _, metrics_id in refs],
            )
        }
        responses: dict[Category, CategoryMetricsResponse] = {}
        for category, metrics_id in refs:
            entity = self._entity(entities, metrics_id, parcel_id)
            if entity.facility_type is not category:
                self._raise_not_found(metrics_id)
            responses[category] = FacilityMetricsResponse(
                id=entity.id.unwrap(),
                buffer=entity.buffer.unwrap(),
                count=entity.count.unwrap(),
                min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
            )
        return responses

    async def _collect_ecology(
        self,
        refs: _Refs,
        parcel_id: ParcelId,
    ) -> dict[Category, CategoryMetricsResponse]:
        """Fetch and map all referenced ecology records in one query."""
        entities = {
            entity.id: entity
            for entity in await self._metrics_repository.get_ecologies_by_ids(
                [metrics_id for _, metrics_id in refs],
            )
        }
        responses: dict[Category, CategoryMetricsResponse] = {}
        for category, metrics_id in refs:
            entity = self._entity(entities, metrics_id, parcel_id)
            if entity.object_type is not category:
                self._raise_not_found(metrics_id)
            responses[category] = EcologyMetricsResponse(
                id=entity.id.unwrap(),
                buffer=entity.buffer.unwrap(),
                coverage_ratio=entity.coverage_ratio.unwrap(),
                count=entity.count.unwrap(),
                min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
                distance_to_large_object=(
                    entity.distance_to_large_object.unwrap() if entity.distance_to_large_object is not None else None
                ),
            )
        return responses

    async def _collect_utility(
        self,
        refs: _Refs,
        parcel_id: ParcelId,
    ) -> dict[Category, CategoryMetricsResponse]:
        """Fetch and map all referenced utility records in one query."""
        entities = {
            entity.id: entity
            for entity in await self._metrics_repository.get_utilities_by_ids(
                [metrics_id for _, metrics_id in refs],
            )
        }
        responses: dict[Category, CategoryMetricsResponse] = {}
        for category, metrics_id in refs:
            entity = self._entity(entities, metrics_id, parcel_id)
            if entity.utility_type is not category:
                self._raise_not_found(metrics_id)
            responses[category] = UtilityMetricsResponse(
                id=entity.id.unwrap(),
                buffer=entity.buffer.unwrap(),
                min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
            )
        return responses

    async def _collect_road_accessibility(
        self,
        refs: _Refs,
        parcel_id: ParcelId,
    ) -> dict[Category, CategoryMetricsResponse]:
        """Fetch and map all referenced road accessibility records in one query."""
        entities = {
            entity.id: entity
            for entity in await self._metrics_repository.get_road_accessibility_by_ids(
                [metrics_id for _, metrics_id in refs],
            )
        }
        responses: dict[Category, CategoryMetricsResponse] = {}
        for category, metrics_id in refs:
            entity = self._entity(entities, metrics_id, parcel_id)
            responses[category] = RoadAccessibilityMetricsResponse(
                id=entity.id.unwrap(),
                buffer=entity.buffer.unwrap(),
                distance_to_paved_road=(
                    entity.distance_to_paved_road.unwrap() if entity.distance_to_paved_road is not None else None
                ),
                road_density_1km=entity.road_density_1km.unwrap(),
            )
        return responses

    async def _collect_geographic_position(
        self,
        refs: _Refs,
        parcel_id: ParcelId,
    ) -> dict[Category, CategoryMetricsResponse]:
        """Fetch and map all referenced geographic position records in one query."""
        entities = {
            entity.id: entity
            for entity in await self._metrics_repository.get_geographic_positions_by_ids(
                [metrics_id for _, metrics_id in refs],
            )
        }
        responses: dict[Category, CategoryMetricsResponse] = {}
        for category, metrics_id in refs:
            entity = self._entity(entities, metrics_id, parcel_id)
            responses[category] = GeographicPositionMetricsResponse(
                id=entity.id.unwrap(),
                buffer=entity.buffer.unwrap(),
                distance_to_major_city=(
                    entity.distance_to_major_city.unwrap() if entity.distance_to_major_city is not None else None
                ),
                city_tier=entity.city_tier.value,
            )
        return responses

    def _entity(
        self,
        entities: dict[InfrastructureMetricsId, EntityT],
        metrics_id: InfrastructureMetricsId,
        parcel_id: ParcelId,
    ) -> EntityT:
        """Return the fetched entity for a reference, or raise not found.

        A missing record or a record belonging to another parcel is treated as
        not found, so the API never leaks the existence of other users' metrics.
        """
        entity = entities.get(metrics_id)
        if entity is None or entity.parcel_id != parcel_id:
            self._raise_not_found(metrics_id)
        return entity

    def _raise_not_found(self, metrics_id: InfrastructureMetricsId) -> NoReturn:
        """Raise a not-found error for the given metrics ID."""
        self._logger.warning("Infrastructure metrics not found: metrics_id=%s", metrics_id.unwrap())
        raise InfrastructureMetricsByIdNotFoundError(str(metrics_id.unwrap()))


__all__ = ("GetInfrastructureMetricsByIdsUseCase",)
