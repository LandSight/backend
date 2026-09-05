"""PostgreSQL metrics repository implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar, cast, override

from sqlalchemy import delete, select

from app.module.infrastructure.application.port import MetricsRepository
from app.module.infrastructure.domain.entity import (
    HospitalMetrics,
    SchoolMetrics,
    ShopMetrics,
    TransitStopMetrics,
    WaterBodyMetrics,
)
from app.module.infrastructure.domain.value_object import (
    Buffer,
    Count,
    CoverageRatio,
    Distance,
    InfrastructureMetricsId,
    ParcelId,
)
from app.module.infrastructure.infrastructure.model import (
    HospitalMetricsModel,
    SchoolMetricsModel,
    ShopMetricsModel,
    TransitStopMetricsModel,
    WaterBodyMetricsModel,
)
from app.platform.database.repository import BaseSQLAlchemyRepository


if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession


ModelT = TypeVar("ModelT")

# Union of all per-category metrics ORM models.
MetricsModel = (
    SchoolMetricsModel | HospitalMetricsModel | ShopMetricsModel | TransitStopMetricsModel | WaterBodyMetricsModel
)


class PostgresMetricsRepository(BaseSQLAlchemyRepository, MetricsRepository):
    """Metrics repository backed by PostgreSQL.

    Stores infrastructure metrics in dedicated tables per category
    (e.g. ``infrastructure.parcel_school_metrics``).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    # ----- Schools -----

    @override
    async def save_schools(self, metrics: SchoolMetrics) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.save_schools`."""
        model = SchoolMetricsModel(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            buffer=metrics.buffer.unwrap(),
            count=metrics.count.unwrap(),
            min_distance_to=metrics.min_distance_to.unwrap() if metrics.min_distance_to is not None else None,
        )
        await self._replace(model, metrics.parcel_id.unwrap(), metrics.buffer.unwrap())

    @override
    async def get_schools(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> SchoolMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_schools`."""
        model = await self._get_latest(SchoolMetricsModel, parcel_id, buffer)
        return self._school_to_domain(model) if model is not None else None

    # ----- Hospitals -----

    @override
    async def save_hospitals(self, metrics: HospitalMetrics) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.save_hospitals`."""
        model = HospitalMetricsModel(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            buffer=metrics.buffer.unwrap(),
            count=metrics.count.unwrap(),
            min_distance_to=metrics.min_distance_to.unwrap() if metrics.min_distance_to is not None else None,
        )
        await self._replace(model, metrics.parcel_id.unwrap(), metrics.buffer.unwrap())

    @override
    async def get_hospitals(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> HospitalMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_hospitals`."""
        model = await self._get_latest(HospitalMetricsModel, parcel_id, buffer)
        return self._hospital_to_domain(model) if model is not None else None

    # ----- Shops -----

    @override
    async def save_shops(self, metrics: ShopMetrics) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.save_shops`."""
        model = ShopMetricsModel(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            buffer=metrics.buffer.unwrap(),
            count=metrics.count.unwrap(),
            min_distance_to=metrics.min_distance_to.unwrap() if metrics.min_distance_to is not None else None,
        )
        await self._replace(model, metrics.parcel_id.unwrap(), metrics.buffer.unwrap())

    @override
    async def get_shops(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> ShopMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_shops`."""
        model = await self._get_latest(ShopMetricsModel, parcel_id, buffer)
        return self._shop_to_domain(model) if model is not None else None

    # ----- Transit stops -----

    @override
    async def save_transit_stops(self, metrics: TransitStopMetrics) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.save_transit_stops`."""
        model = TransitStopMetricsModel(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            buffer=metrics.buffer.unwrap(),
            count=metrics.count.unwrap(),
            min_distance_to=metrics.min_distance_to.unwrap() if metrics.min_distance_to is not None else None,
        )
        await self._replace(model, metrics.parcel_id.unwrap(), metrics.buffer.unwrap())

    @override
    async def get_transit_stops(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> TransitStopMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_transit_stops`."""
        model = await self._get_latest(TransitStopMetricsModel, parcel_id, buffer)
        return self._transit_stop_to_domain(model) if model is not None else None

    # ----- Water bodies -----

    @override
    async def save_water_bodies(self, metrics: WaterBodyMetrics) -> None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.save_water_bodies`."""
        model = WaterBodyMetricsModel(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            buffer=metrics.buffer.unwrap(),
            count=metrics.count.unwrap(),
            min_distance_to=metrics.min_distance_to.unwrap() if metrics.min_distance_to is not None else None,
            coverage_ratio=metrics.coverage_ratio.unwrap(),
        )
        await self._replace(model, metrics.parcel_id.unwrap(), metrics.buffer.unwrap())

    @override
    async def get_water_bodies(
        self,
        parcel_id: ParcelId,
        buffer: Buffer | None = None,
    ) -> WaterBodyMetrics | None:
        """See :class:`app.module.infrastructure.application.port.MetricsRepository.get_water_bodies`."""
        model = await self._get_latest(WaterBodyMetricsModel, parcel_id, buffer)
        return self._water_body_to_domain(model) if model is not None else None

    # ----- Helpers -----

    async def _replace(self, model: MetricsModel, parcel_id: UUID, buffer: int) -> None:
        """Replace any existing metrics row for the (parcel, buffer) pair.

        MVP keeps at most one row per (parcel, category, buffer): recalculating
        overwrites the previous result instead of accumulating history.
        """
        model_cls = type(model)
        stmt = delete(model_cls).where(
            model_cls.parcel_id == parcel_id,
            model_cls.buffer == buffer,
        )
        await self._session.execute(stmt)
        self._session.add(model)

    async def _get_latest(
        self,
        model_cls: type[ModelT],
        parcel_id: ParcelId,
        buffer: Buffer | None,
    ) -> ModelT | None:
        """Retrieve the most recent metrics row for a parcel.

        If ``buffer`` is provided, returns the row for that exact buffer radius.
        Otherwise, returns the most recent row (ordered by ``created_at DESC``).
        """
        model_attrs = cast("Any", model_cls)
        stmt = select(model_cls).where(model_attrs.parcel_id == parcel_id.unwrap())
        if buffer is not None:
            stmt = stmt.where(model_attrs.buffer == buffer.unwrap())
        stmt = stmt.order_by(model_attrs.created_at.desc()).limit(1)

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    def _school_to_domain(model: SchoolMetricsModel) -> SchoolMetrics:
        """Convert an ORM model to a domain entity."""
        return SchoolMetrics(
            id=InfrastructureMetricsId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            buffer=Buffer(model.buffer),
            count=Count(model.count),
            min_distance_to=Distance(model.min_distance_to) if model.min_distance_to is not None else None,
        )

    @staticmethod
    def _hospital_to_domain(model: HospitalMetricsModel) -> HospitalMetrics:
        """Convert an ORM model to a domain entity."""
        return HospitalMetrics(
            id=InfrastructureMetricsId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            buffer=Buffer(model.buffer),
            count=Count(model.count),
            min_distance_to=Distance(model.min_distance_to) if model.min_distance_to is not None else None,
        )

    @staticmethod
    def _shop_to_domain(model: ShopMetricsModel) -> ShopMetrics:
        """Convert an ORM model to a domain entity."""
        return ShopMetrics(
            id=InfrastructureMetricsId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            buffer=Buffer(model.buffer),
            count=Count(model.count),
            min_distance_to=Distance(model.min_distance_to) if model.min_distance_to is not None else None,
        )

    @staticmethod
    def _transit_stop_to_domain(model: TransitStopMetricsModel) -> TransitStopMetrics:
        """Convert an ORM model to a domain entity."""
        return TransitStopMetrics(
            id=InfrastructureMetricsId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            buffer=Buffer(model.buffer),
            count=Count(model.count),
            min_distance_to=Distance(model.min_distance_to) if model.min_distance_to is not None else None,
        )

    @staticmethod
    def _water_body_to_domain(model: WaterBodyMetricsModel) -> WaterBodyMetrics:
        """Convert an ORM model to a domain entity."""
        return WaterBodyMetrics(
            id=InfrastructureMetricsId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            buffer=Buffer(model.buffer),
            count=Count(model.count),
            min_distance_to=Distance(model.min_distance_to) if model.min_distance_to is not None else None,
            coverage_ratio=CoverageRatio(model.coverage_ratio),
        )


__all__ = ("PostgresMetricsRepository",)
