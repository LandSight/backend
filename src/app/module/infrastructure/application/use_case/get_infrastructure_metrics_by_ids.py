"""Get infrastructure metrics by IDs use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from app.module.infrastructure.application.dto.command import (
    GetInfrastructureMetricsByIdsCommand,
)
from app.module.infrastructure.application.dto.response import (
    HospitalMetricsResponse,
    InfrastructureMetricsResponse,
    SchoolMetricsResponse,
    ShopMetricsResponse,
    TransitStopMetricsResponse,
    WaterBodyMetricsResponse,
)
from app.module.infrastructure.application.error import InfrastructureMetricsByIdNotFoundError
from app.module.infrastructure.domain.value_object import Category, InfrastructureMetricsId, ParcelId
from app.module.shared.application.error import ForbiddenError
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from typing import NoReturn

    from app.module.infrastructure.application.port import MetricsPermissionService, MetricsRepository


class GetInfrastructureMetricsByIdsUseCase(
    BaseUseCase[GetInfrastructureMetricsByIdsCommand, InfrastructureMetricsResponse]
):
    """Retrieve specific infrastructure metrics records by their IDs.

    Each reference selects the dedicated metrics table via its category. All
    records must belong to the requested parcel; access is granted only when the
    current user owns that parcel.
    """

    def __init__(
        self,
        metrics_repository: MetricsRepository,
        metrics_permission_service: MetricsPermissionService,
    ) -> None:
        self._metrics_repository = metrics_repository
        self._metrics_permission_service = metrics_permission_service
        self._logger = get_logger("app.infrastructure.use_case.get_infrastructure_metrics_by_ids")

        self._handlers: dict[
            Category,
            Callable[[ParcelId, InfrastructureMetricsId], Awaitable[Any]],
        ] = {
            Category.SCHOOL: self._handle_schools,
            Category.HOSPITAL: self._handle_hospitals,
            Category.SHOP: self._handle_shops,
            Category.TRANSIT_STOP: self._handle_transit_stops,
            Category.WATER_BODY: self._handle_water_bodies,
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
        results: dict[Category, Any] = {}

        for metric in command.metrics:
            category = Category(metric.category)
            metrics_id = InfrastructureMetricsId(metric.metrics_id)
            results[category] = await self._handlers[category](parcel_id, metrics_id)

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
        parcel_id: ParcelId,
        metrics_id: InfrastructureMetricsId,
    ) -> SchoolMetricsResponse:
        """Load school metrics by ID and convert them to a response."""
        entity = await self._metrics_repository.get_schools_by_id(metrics_id)
        if entity is None:
            self._raise_not_found(metrics_id)
        if entity.parcel_id != parcel_id:
            self._raise_not_found(metrics_id)
        return SchoolMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
        )

    async def _handle_hospitals(
        self,
        parcel_id: ParcelId,
        metrics_id: InfrastructureMetricsId,
    ) -> HospitalMetricsResponse:
        """Load hospital metrics by ID and convert them to a response."""
        entity = await self._metrics_repository.get_hospitals_by_id(metrics_id)
        if entity is None:
            self._raise_not_found(metrics_id)
        if entity.parcel_id != parcel_id:
            self._raise_not_found(metrics_id)
        return HospitalMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
        )

    async def _handle_shops(
        self,
        parcel_id: ParcelId,
        metrics_id: InfrastructureMetricsId,
    ) -> ShopMetricsResponse:
        """Load shop metrics by ID and convert them to a response."""
        entity = await self._metrics_repository.get_shops_by_id(metrics_id)
        if entity is None:
            self._raise_not_found(metrics_id)
        if entity.parcel_id != parcel_id:
            self._raise_not_found(metrics_id)
        return ShopMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
        )

    async def _handle_transit_stops(
        self,
        parcel_id: ParcelId,
        metrics_id: InfrastructureMetricsId,
    ) -> TransitStopMetricsResponse:
        """Load transit stop metrics by ID and convert them to a response."""
        entity = await self._metrics_repository.get_transit_stops_by_id(metrics_id)
        if entity is None:
            self._raise_not_found(metrics_id)
        if entity.parcel_id != parcel_id:
            self._raise_not_found(metrics_id)
        return TransitStopMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
        )

    async def _handle_water_bodies(
        self,
        parcel_id: ParcelId,
        metrics_id: InfrastructureMetricsId,
    ) -> WaterBodyMetricsResponse:
        """Load water body metrics by ID and convert them to a response."""
        entity = await self._metrics_repository.get_water_bodies_by_id(metrics_id)
        if entity is None:
            self._raise_not_found(metrics_id)
        if entity.parcel_id != parcel_id:
            self._raise_not_found(metrics_id)
        return WaterBodyMetricsResponse(
            id=entity.id.unwrap(),
            buffer=entity.buffer.unwrap(),
            count=entity.count.unwrap(),
            min_distance_to=entity.min_distance_to.unwrap() if entity.min_distance_to is not None else None,
            coverage_ratio=entity.coverage_ratio.unwrap(),
        )

    def _raise_not_found(self, metrics_id: InfrastructureMetricsId) -> NoReturn:
        """Raise a not-found error for the given metrics ID."""
        self._logger.warning("Infrastructure metrics not found: metrics_id=%s", metrics_id.unwrap())
        raise InfrastructureMetricsByIdNotFoundError(str(metrics_id.unwrap()))


__all__ = ("GetInfrastructureMetricsByIdsUseCase",)
