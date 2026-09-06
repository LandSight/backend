"""PostgreSQL metrics repository implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from sqlalchemy import delete, select

from app.module.climate.application.port import MetricsRepository
from app.module.climate.domain.entity import ClimateMetrics
from app.module.climate.domain.value_object.metric import (
    ClimateMetricsId,
    ParcelId,
    Percentage,
    Precipitation,
    Temperature,
)
from app.module.climate.infrastructure.model import ClimateMetricsModel
from app.platform.database.repository import BaseSQLAlchemyRepository


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class PostgresMetricsRepository(BaseSQLAlchemyRepository, MetricsRepository):
    """Metrics repository backed by PostgreSQL.

    Stores climate metrics in the ``climate.metrics`` table.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @override
    async def save(self, metrics: ClimateMetrics) -> ClimateMetrics:
        """See :class:`app.module.climate.application.port.MetricsRepository.save`."""
        model = ClimateMetricsModel(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            mean_annual_temperature=metrics.mean_annual_temperature.unwrap(),
            annual_precipitation=metrics.annual_precipitation.unwrap(),
            temperature_seasonality=metrics.temperature_seasonality.unwrap(),
            precipitation_seasonality=metrics.precipitation_seasonality.unwrap(),
            max_temperature_warmest_month=metrics.max_temperature_warmest_month.unwrap(),
            min_temperature_coldest_month=metrics.min_temperature_coldest_month.unwrap(),
            precipitation_wettest_month=metrics.precipitation_wettest_month.unwrap(),
            precipitation_driest_month=metrics.precipitation_driest_month.unwrap(),
        )
        # MVP keeps at most one row per parcel: recalculating overwrites the
        # previous snapshot instead of accumulating history.
        await self._session.execute(
            delete(ClimateMetricsModel).where(ClimateMetricsModel.parcel_id == metrics.parcel_id.unwrap())
        )
        self._session.add(model)
        await self._session.flush()

        return self._to_domain(model)

    @override
    async def get(self, metrics_id: ClimateMetricsId) -> ClimateMetrics | None:
        """See :class:`app.module.climate.application.port.MetricsRepository.get`."""
        result = await self._session.execute(
            select(ClimateMetricsModel).where(ClimateMetricsModel.id == metrics_id.unwrap()),
        )
        model = result.scalar_one_or_none()

        return self._to_domain(model) if model is not None else None

    @override
    async def get_parcel_metrics(self, parcel_id: ParcelId) -> ClimateMetrics | None:
        """See :class:`app.module.climate.application.port.MetricsRepository.get_parcel_metrics`."""
        result = await self._session.execute(
            select(ClimateMetricsModel)
            .where(ClimateMetricsModel.parcel_id == parcel_id.unwrap())
            .order_by(ClimateMetricsModel.created_at.desc())
            .limit(1),
        )
        model = result.scalar_one_or_none()

        return self._to_domain(model) if model is not None else None

    @staticmethod
    def _to_domain(model: ClimateMetricsModel) -> ClimateMetrics:
        """Convert an ORM model to a domain entity."""
        return ClimateMetrics(
            id=ClimateMetricsId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            mean_annual_temperature=Temperature(model.mean_annual_temperature),
            annual_precipitation=Precipitation(model.annual_precipitation),
            temperature_seasonality=Temperature(model.temperature_seasonality),
            precipitation_seasonality=Percentage(model.precipitation_seasonality),
            max_temperature_warmest_month=Temperature(model.max_temperature_warmest_month),
            min_temperature_coldest_month=Temperature(model.min_temperature_coldest_month),
            precipitation_wettest_month=Precipitation(model.precipitation_wettest_month),
            precipitation_driest_month=Precipitation(model.precipitation_driest_month),
            created_at=model.created_at,
        )


__all__ = ("PostgresMetricsRepository",)
