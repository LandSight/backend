"""Get infrastructure metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from app.module.infrastructure.application.dto.command import (
    GetInfrastructureMetricsCommand,
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
from app.module.infrastructure.domain.value_object import Buffer, Category, ParcelId
from app.module.shared.application.error import ForbiddenError
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from app.module.infrastructure.application.port import MetricsPermissionService, MetricsRepository

    _Handler = Callable[[ParcelId, Buffer, Category], Awaitable[Any]]


class GetInfrastructureMetricsUseCase(BaseUseCase[GetInfrastructureMetricsCommand, InfrastructureMetricsResponse]):
    """Get infrastructure metrics for a parcel.

    Retrieves metrics for requested categories with specified buffers. If a
    category has no metrics, it is absent from the response.
    """

    def __init__(
        self,
        metrics_repository: MetricsRepository,
        metrics_permission_service: MetricsPermissionService,
    ) -> None:
        self._metrics_repository = metrics_repository
        self._metrics_permission_service = metrics_permission_service
        self._logger = get_logger("app.infrastructure.use_case.get_infrastructure_metrics")

        facility = self._handle_facility
        ecology = self._handle_ecology
        utility = self._handle_utility
        self._handlers: dict[Category, _Handler] = {
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
            Category.ROAD_ACCESSIBILITY: self._handle_road_accessibility,
            Category.GEOGRAPHIC_POSITION: self._handle_geographic_position,
        }

    @override
    async def __call__(self, command: GetInfrastructureMetricsCommand) -> InfrastructureMetricsResponse:
        self._logger.info("Getting infrastructure metrics: parcel_id=%s", command.parcel_id)

        if not await self._metrics_permission_service.user_can_view_parcel_metrics(
            command.current_user_id,
            command.parcel_id,
        ):
            reason = f"User is not allowed to view metrics for parcel '{command.parcel_id}'"
            raise ForbiddenError(reason)

        parcel_id = ParcelId(command.parcel_id)

        results: dict[str, Any] = {}

        for category_request in command.categories:
            category = self._parse_category(category_request.category)
            buffer = Buffer(category_request.buffer)

            result = await self._handlers[category](parcel_id, buffer, category)
            if result is not None:
                results[category.value] = result

        self._logger.info(
            "Metrics retrieved: parcel_id=%s categories=%s",
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
        parcel_id: ParcelId,
        buffer: Buffer,
        category: Category,
    ) -> FacilityMetricsResponse | None:
        entity = await self._metrics_repository.get_facility(parcel_id, category, buffer)
        if entity is None:
            return None
        return FacilityMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
        )

    async def _handle_ecology(
        self,
        parcel_id: ParcelId,
        buffer: Buffer,
        category: Category,
    ) -> EcologyMetricsResponse | None:
        entity = await self._metrics_repository.get_ecology(parcel_id, category, buffer)
        if entity is None:
            return None
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
        buffer: Buffer,
        category: Category,
    ) -> UtilityMetricsResponse | None:
        entity = await self._metrics_repository.get_utility(parcel_id, category, buffer)
        if entity is None:
            return None
        return UtilityMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
        )

    async def _handle_road_accessibility(
        self,
        parcel_id: ParcelId,
        buffer: Buffer,
        category: Category,  # noqa: ARG002
    ) -> RoadAccessibilityMetricsResponse | None:
        entity = await self._metrics_repository.get_road_accessibility(parcel_id, buffer)
        if entity is None:
            return None
        return RoadAccessibilityMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            distance_to_paved_road=(
                entity.distance_to_paved_road.unwrap() if entity.distance_to_paved_road is not None else None
            ),
            distance_to_main_road=(
                entity.distance_to_main_road.unwrap() if entity.distance_to_main_road is not None else None
            ),
            distance_to_any_road=(
                entity.distance_to_any_road.unwrap() if entity.distance_to_any_road is not None else None
            ),
            road_density_1km=entity.road_density_1km.unwrap(),
        )

    async def _handle_geographic_position(
        self,
        parcel_id: ParcelId,
        buffer: Buffer,
        category: Category,  # noqa: ARG002
    ) -> GeographicPositionMetricsResponse | None:
        entity = await self._metrics_repository.get_geographic_position(parcel_id, buffer)
        if entity is None:
            return None
        return GeographicPositionMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            distance_to_regional_center=(
                entity.distance_to_regional_center.unwrap() if entity.distance_to_regional_center is not None else None
            ),
            distance_to_district_center=(
                entity.distance_to_district_center.unwrap() if entity.distance_to_district_center is not None else None
            ),
            distance_to_settlement=(
                entity.distance_to_settlement.unwrap() if entity.distance_to_settlement is not None else None
            ),
        )


__all__ = ("GetInfrastructureMetricsUseCase",)
