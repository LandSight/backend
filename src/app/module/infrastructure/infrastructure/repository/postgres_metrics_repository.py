"""PostgreSQL metrics repository implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar, cast, override

from sqlalchemy import delete as sa_delete, select

from app.module.infrastructure.application.port import MetricsRepository
from app.module.infrastructure.domain.entity import (
    EcologyMetrics,
    FacilityMetrics,
    GeographicPositionMetrics,
    RoadAccessibilityMetrics,
    UtilityMetrics,
)
from app.module.infrastructure.domain.value_object import (
    Buffer,
    Category,
    Count,
    CoverageRatio,
    Density,
    Distance,
    InfrastructureMetricsId,
    ParcelId,
)
from app.module.infrastructure.infrastructure.model import (
    EcologyMetricsModel,
    FacilityMetricsModel,
    GeographicPositionMetricsModel,
    RoadAccessibilityMetricsModel,
    UtilityMetricsModel,
)
from app.platform.database.repository import BaseSQLAlchemyRepository


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


ModelT = TypeVar("ModelT")

# Union of all metrics family ORM models.
MetricsModel = (
    FacilityMetricsModel
    | EcologyMetricsModel
    | UtilityMetricsModel
    | RoadAccessibilityMetricsModel
    | GeographicPositionMetricsModel
)


class PostgresMetricsRepository(BaseSQLAlchemyRepository, MetricsRepository):
    """Metrics repository backed by PostgreSQL.

    Stores infrastructure metrics in dedicated family tables
    (``parcel_facility_metrics``, ``parcel_ecology_metrics``,
    ``parcel_utility_metrics``, ...). Categories sharing a family are
    disambiguated by a type column.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    # ----- Facility -----

    @override
    async def save_facility(self, metrics: FacilityMetrics) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.save_facility`."""
        model = FacilityMetricsModel(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            buffer=metrics.buffer.unwrap(),
            facility_type=metrics.facility_type.value,
            count=metrics.count.unwrap(),
            min_distance_to=metrics.min_distance_to.unwrap() if metrics.min_distance_to is not None else None,
        )
        await self._insert(model)

    @override
    async def get_facility(
        self,
        parcel_id: ParcelId,
        category: Category,
        buffer: Buffer | None = None,
    ) -> FacilityMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_facility`."""
        model = await self._get_latest(
            FacilityMetricsModel,
            parcel_id,
            buffer,
            type_column="facility_type",
            type_value=category.value,
        )
        return self._facility_to_domain(model) if model is not None else None

    @override
    async def get_facility_by_id(self, metrics_id: InfrastructureMetricsId) -> FacilityMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_facility_by_id`."""
        model = await self._get_by_id(FacilityMetricsModel, metrics_id)
        return self._facility_to_domain(model) if model is not None else None

    @override
    async def get_facilities_by_ids(
        self,
        metrics_ids: list[InfrastructureMetricsId],
    ) -> list[FacilityMetrics]:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_facilities_by_ids`."""
        models = await self._get_by_ids(FacilityMetricsModel, metrics_ids)
        return [self._facility_to_domain(model) for model in models]

    @override
    async def delete_facility(self, metrics_ids: list[InfrastructureMetricsId]) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.delete_facility`."""
        await self._delete_by_ids(FacilityMetricsModel, metrics_ids)

    # ----- Ecology -----

    @override
    async def save_ecology(self, metrics: EcologyMetrics) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.save_ecology`."""
        model = EcologyMetricsModel(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            buffer=metrics.buffer.unwrap(),
            object_type=metrics.object_type.value,
            coverage_ratio=metrics.coverage_ratio.unwrap(),
            count=metrics.count.unwrap(),
            min_distance_to=metrics.min_distance_to.unwrap() if metrics.min_distance_to is not None else None,
            distance_to_large_object=(
                metrics.distance_to_large_object.unwrap() if metrics.distance_to_large_object is not None else None
            ),
        )
        await self._insert(model)

    @override
    async def get_ecology(
        self,
        parcel_id: ParcelId,
        category: Category,
        buffer: Buffer | None = None,
    ) -> EcologyMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_ecology`."""
        model = await self._get_latest(
            EcologyMetricsModel,
            parcel_id,
            buffer,
            type_column="object_type",
            type_value=category.value,
        )
        return self._ecology_to_domain(model) if model is not None else None

    @override
    async def get_ecology_by_id(self, metrics_id: InfrastructureMetricsId) -> EcologyMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_ecology_by_id`."""
        model = await self._get_by_id(EcologyMetricsModel, metrics_id)
        return self._ecology_to_domain(model) if model is not None else None

    @override
    async def get_ecologies_by_ids(
        self,
        metrics_ids: list[InfrastructureMetricsId],
    ) -> list[EcologyMetrics]:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_ecologies_by_ids`."""
        models = await self._get_by_ids(EcologyMetricsModel, metrics_ids)
        return [self._ecology_to_domain(model) for model in models]

    @override
    async def delete_ecology(self, metrics_ids: list[InfrastructureMetricsId]) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.delete_ecology`."""
        await self._delete_by_ids(EcologyMetricsModel, metrics_ids)

    # ----- Utility -----

    @override
    async def save_utility(self, metrics: UtilityMetrics) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.save_utility`."""
        model = UtilityMetricsModel(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            buffer=metrics.buffer.unwrap(),
            utility_type=metrics.utility_type.value,
            min_distance_to=metrics.min_distance_to.unwrap() if metrics.min_distance_to is not None else None,
        )
        await self._insert(model)

    @override
    async def get_utility(
        self,
        parcel_id: ParcelId,
        category: Category,
        buffer: Buffer | None = None,
    ) -> UtilityMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_utility`."""
        model = await self._get_latest(
            UtilityMetricsModel,
            parcel_id,
            buffer,
            type_column="utility_type",
            type_value=category.value,
        )
        return self._utility_to_domain(model) if model is not None else None

    @override
    async def get_utility_by_id(self, metrics_id: InfrastructureMetricsId) -> UtilityMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_utility_by_id`."""
        model = await self._get_by_id(UtilityMetricsModel, metrics_id)
        return self._utility_to_domain(model) if model is not None else None

    @override
    async def get_utilities_by_ids(
        self,
        metrics_ids: list[InfrastructureMetricsId],
    ) -> list[UtilityMetrics]:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_utilities_by_ids`."""
        models = await self._get_by_ids(UtilityMetricsModel, metrics_ids)
        return [self._utility_to_domain(model) for model in models]

    @override
    async def delete_utility(self, metrics_ids: list[InfrastructureMetricsId]) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.delete_utility`."""
        await self._delete_by_ids(UtilityMetricsModel, metrics_ids)

    # ----- Road accessibility -----

    @override
    async def save_road_accessibility(self, metrics: RoadAccessibilityMetrics) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.save_road_accessibility`."""
        model = RoadAccessibilityMetricsModel(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            buffer=metrics.buffer.unwrap(),
            distance_to_paved_road=(
                metrics.distance_to_paved_road.unwrap() if metrics.distance_to_paved_road is not None else None
            ),
            distance_to_main_road=(
                metrics.distance_to_main_road.unwrap() if metrics.distance_to_main_road is not None else None
            ),
            distance_to_any_road=(
                metrics.distance_to_any_road.unwrap() if metrics.distance_to_any_road is not None else None
            ),
            road_density_1km=metrics.road_density_1km.unwrap(),
        )
        await self._insert(model)

    @override
    async def get_road_accessibility(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> RoadAccessibilityMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_road_accessibility`."""
        model = await self._get_latest(RoadAccessibilityMetricsModel, parcel_id, buffer)
        return self._road_accessibility_to_domain(model) if model is not None else None

    @override
    async def get_road_accessibility_by_id(
        self,
        metrics_id: InfrastructureMetricsId,
    ) -> RoadAccessibilityMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_road_accessibility_by_id`."""
        model = await self._get_by_id(RoadAccessibilityMetricsModel, metrics_id)
        return self._road_accessibility_to_domain(model) if model is not None else None

    @override
    async def get_road_accessibility_by_ids(
        self,
        metrics_ids: list[InfrastructureMetricsId],
    ) -> list[RoadAccessibilityMetrics]:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_road_accessibility_by_ids`."""
        models = await self._get_by_ids(RoadAccessibilityMetricsModel, metrics_ids)
        return [self._road_accessibility_to_domain(model) for model in models]

    @override
    async def delete_road_accessibility(self, metrics_ids: list[InfrastructureMetricsId]) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.delete_road_accessibility`."""
        await self._delete_by_ids(RoadAccessibilityMetricsModel, metrics_ids)

    # ----- Geographic position -----

    @override
    async def save_geographic_position(self, metrics: GeographicPositionMetrics) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.save_geographic_position`."""
        model = GeographicPositionMetricsModel(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            buffer=metrics.buffer.unwrap(),
            distance_to_regional_center=(
                metrics.distance_to_regional_center.unwrap()
                if metrics.distance_to_regional_center is not None
                else None
            ),
            distance_to_district_center=(
                metrics.distance_to_district_center.unwrap()
                if metrics.distance_to_district_center is not None
                else None
            ),
            distance_to_settlement=(
                metrics.distance_to_settlement.unwrap() if metrics.distance_to_settlement is not None else None
            ),
        )
        await self._insert(model)

    @override
    async def get_geographic_position(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> GeographicPositionMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_geographic_position`."""
        model = await self._get_latest(GeographicPositionMetricsModel, parcel_id, buffer)
        return self._geographic_position_to_domain(model) if model is not None else None

    @override
    async def get_geographic_position_by_id(
        self,
        metrics_id: InfrastructureMetricsId,
    ) -> GeographicPositionMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_geographic_position_by_id`."""
        model = await self._get_by_id(GeographicPositionMetricsModel, metrics_id)
        return self._geographic_position_to_domain(model) if model is not None else None

    @override
    async def get_geographic_positions_by_ids(
        self,
        metrics_ids: list[InfrastructureMetricsId],
    ) -> list[GeographicPositionMetrics]:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_geographic_positions_by_ids`."""
        models = await self._get_by_ids(GeographicPositionMetricsModel, metrics_ids)
        return [self._geographic_position_to_domain(model) for model in models]

    @override
    async def delete_geographic_position(self, metrics_ids: list[InfrastructureMetricsId]) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.delete_geographic_position`."""
        await self._delete_by_ids(GeographicPositionMetricsModel, metrics_ids)

    # ----- Helpers -----

    async def _delete_by_ids(
        self,
        model_cls: type[ModelT],
        metrics_ids: list[InfrastructureMetricsId],
    ) -> None:
        """Delete rows of one metrics family by their IDs."""
        if not metrics_ids:
            return
        ids = [metrics_id.unwrap() for metrics_id in metrics_ids]
        await self._session.execute(sa_delete(model_cls).where(cast("Any", model_cls).id.in_(ids)))
        await self._session.flush()

    async def _insert(self, model: MetricsModel) -> None:
        """Append a new metrics row.

        Append-only: every calculation is stored as a new snapshot so that
        analyses can keep referencing the exact metrics they were computed from.
        """
        self._session.add(model)
        await self._session.flush()

    async def _get_by_id(
        self,
        model_cls: type[ModelT],
        metrics_id: InfrastructureMetricsId,
    ) -> ModelT | None:
        """Retrieve a metrics row by its primary key."""
        result = await self._session.execute(
            select(model_cls).where(cast("Any", model_cls).id == metrics_id.unwrap()),
        )
        return result.scalar_one_or_none()

    async def _get_by_ids(
        self,
        model_cls: type[ModelT],
        metrics_ids: list[InfrastructureMetricsId],
    ) -> list[ModelT]:
        """Retrieve several metrics rows of one family in a single query."""
        if not metrics_ids:
            return []
        ids = [metrics_id.unwrap() for metrics_id in metrics_ids]
        result = await self._session.execute(
            select(model_cls).where(cast("Any", model_cls).id.in_(ids)),
        )
        return list(result.scalars().all())

    async def _get_latest(
        self,
        model_cls: type[ModelT],
        parcel_id: ParcelId,
        buffer: Buffer | None,
        *,
        type_column: str | None = None,
        type_value: str | None = None,
    ) -> ModelT | None:
        """Retrieve the most recent metrics row for a parcel.

        If ``type_column`` is provided, rows are additionally filtered by the
        category type. If ``buffer`` is provided, returns the row for that exact
        buffer radius. Otherwise, returns the most recent row (ordered by
        ``created_at DESC``).
        """
        model_attrs = cast("Any", model_cls)
        stmt = select(model_cls).where(model_attrs.parcel_id == parcel_id.unwrap())
        if type_column is not None:
            stmt = stmt.where(getattr(model_attrs, type_column) == type_value)
        if buffer is not None:
            stmt = stmt.where(model_attrs.buffer == buffer.unwrap())
        stmt = stmt.order_by(model_attrs.created_at.desc()).limit(1)

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    def _facility_to_domain(model: FacilityMetricsModel) -> FacilityMetrics:
        """Convert an ORM model to a domain entity."""
        return FacilityMetrics(
            id=InfrastructureMetricsId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            buffer=Buffer(model.buffer),
            facility_type=Category(model.facility_type),
            count=Count(model.count),
            min_distance_to=Distance(model.min_distance_to) if model.min_distance_to is not None else None,
        )

    @staticmethod
    def _ecology_to_domain(model: EcologyMetricsModel) -> EcologyMetrics:
        """Convert an ORM model to a domain entity."""
        return EcologyMetrics(
            id=InfrastructureMetricsId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            buffer=Buffer(model.buffer),
            object_type=Category(model.object_type),
            coverage_ratio=CoverageRatio(model.coverage_ratio),
            count=Count(model.count),
            min_distance_to=Distance(model.min_distance_to) if model.min_distance_to is not None else None,
            distance_to_large_object=(
                Distance(model.distance_to_large_object) if model.distance_to_large_object is not None else None
            ),
        )

    @staticmethod
    def _utility_to_domain(model: UtilityMetricsModel) -> UtilityMetrics:
        """Convert an ORM model to a domain entity."""
        return UtilityMetrics(
            id=InfrastructureMetricsId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            buffer=Buffer(model.buffer),
            utility_type=Category(model.utility_type),
            min_distance_to=Distance(model.min_distance_to) if model.min_distance_to is not None else None,
        )

    @staticmethod
    def _road_accessibility_to_domain(model: RoadAccessibilityMetricsModel) -> RoadAccessibilityMetrics:
        """Convert an ORM model to a domain entity."""
        return RoadAccessibilityMetrics(
            id=InfrastructureMetricsId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            buffer=Buffer(model.buffer),
            distance_to_paved_road=(
                Distance(model.distance_to_paved_road) if model.distance_to_paved_road is not None else None
            ),
            distance_to_main_road=(
                Distance(model.distance_to_main_road) if model.distance_to_main_road is not None else None
            ),
            distance_to_any_road=(
                Distance(model.distance_to_any_road) if model.distance_to_any_road is not None else None
            ),
            road_density_1km=Density(model.road_density_1km),
        )

    @staticmethod
    def _geographic_position_to_domain(model: GeographicPositionMetricsModel) -> GeographicPositionMetrics:
        """Convert an ORM model to a domain entity."""
        return GeographicPositionMetrics(
            id=InfrastructureMetricsId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            buffer=Buffer(model.buffer),
            distance_to_regional_center=(
                Distance(model.distance_to_regional_center) if model.distance_to_regional_center is not None else None
            ),
            distance_to_district_center=(
                Distance(model.distance_to_district_center) if model.distance_to_district_center is not None else None
            ),
            distance_to_settlement=(
                Distance(model.distance_to_settlement) if model.distance_to_settlement is not None else None
            ),
        )


__all__ = ("PostgresMetricsRepository",)
