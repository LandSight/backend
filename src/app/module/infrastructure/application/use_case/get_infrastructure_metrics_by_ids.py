"""Get infrastructure metrics by IDs use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

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
from app.module.infrastructure.domain.value_object import Category, InfrastructureMetricsId, ParcelId
from app.module.shared.application.error import ForbiddenError
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from typing import NoReturn

    from app.module.infrastructure.application.port import MetricsPermissionService, MetricsRepository

    _Handler = Callable[[ParcelId, InfrastructureMetricsId, Category], Awaitable[Any]]


class GetInfrastructureMetricsByIdsUseCase(
    BaseUseCase[GetInfrastructureMetricsByIdsCommand, InfrastructureMetricsResponse]
):
    """Retrieve specific infrastructure metrics records by their IDs.

    Each reference selects the dedicated metrics family table via its category.
    All records must belong to the requested parcel; access is granted only when
    the current user owns that parcel.
    """

    def __init__(
        self,
        metrics_repository: MetricsRepository,
        metrics_permission_service: MetricsPermissionService,
    ) -> None:
        self._metrics_repository = metrics_repository
        self._metrics_permission_service = metrics_permission_service
        self._logger = get_logger("app.infrastructure.use_case.get_infrastructure_metrics_by_ids")

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
        results: dict[str, Any] = {}

        for metric in command.metrics:
            category = self._parse_category(metric.category)
            metrics_id = InfrastructureMetricsId(metric.metrics_id)
            results[category.value] = await self._handlers[category](parcel_id, metrics_id, category)

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
        parcel_id: ParcelId,
        metrics_id: InfrastructureMetricsId,
        category: Category,  # noqa: ARG002
    ) -> FacilityMetricsResponse:
        entity = await self._metrics_repository.get_facility_by_id(metrics_id)
        if entity is None or entity.parcel_id != parcel_id:
            self._raise_not_found(metrics_id)
        return FacilityMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
        )

    async def _handle_ecology(
        self,
        parcel_id: ParcelId,
        metrics_id: InfrastructureMetricsId,
        category: Category,  # noqa: ARG002
    ) -> EcologyMetricsResponse:
        entity = await self._metrics_repository.get_ecology_by_id(metrics_id)
        if entity is None or entity.parcel_id != parcel_id:
            self._raise_not_found(metrics_id)
        return EcologyMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            coverage_ratio=entity.coverage_ratio.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
            distance_to_large_object=(
                entity.distance_to_large_object.unwrap() if entity.distance_to_large_object is not None else None
            ),
        )

    async def _handle_utility(
        self,
        parcel_id: ParcelId,
        metrics_id: InfrastructureMetricsId,
        category: Category,  # noqa: ARG002
    ) -> UtilityMetricsResponse:
        entity = await self._metrics_repository.get_utility_by_id(metrics_id)
        if entity is None or entity.parcel_id != parcel_id:
            self._raise_not_found(metrics_id)
        return UtilityMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
        )

    async def _handle_road_accessibility(
        self,
        parcel_id: ParcelId,
        metrics_id: InfrastructureMetricsId,
        category: Category,  # noqa: ARG002
    ) -> RoadAccessibilityMetricsResponse:
        entity = await self._metrics_repository.get_road_accessibility_by_id(metrics_id)
        if entity is None or entity.parcel_id != parcel_id:
            self._raise_not_found(metrics_id)
        return RoadAccessibilityMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            distance_to_paved_road=(
                entity.distance_to_paved_road.unwrap() if entity.distance_to_paved_road is not None else None
            ),
            road_density_1km=entity.road_density_1km.unwrap(),
        )

    async def _handle_geographic_position(
        self,
        parcel_id: ParcelId,
        metrics_id: InfrastructureMetricsId,
        category: Category,  # noqa: ARG002
    ) -> GeographicPositionMetricsResponse:
        entity = await self._metrics_repository.get_geographic_position_by_id(metrics_id)
        if entity is None or entity.parcel_id != parcel_id:
            self._raise_not_found(metrics_id)
        return GeographicPositionMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            distance_to_major_city=(
                entity.distance_to_major_city.unwrap() if entity.distance_to_major_city is not None else None
            ),
            city_tier=entity.city_tier.value,
        )

    def _raise_not_found(self, metrics_id: InfrastructureMetricsId) -> NoReturn:
        """Raise a not-found error for the given metrics ID."""
        self._logger.warning("Infrastructure metrics not found: metrics_id=%s", metrics_id.unwrap())
        raise InfrastructureMetricsByIdNotFoundError(str(metrics_id.unwrap()))


__all__ = ("GetInfrastructureMetricsByIdsUseCase",)
