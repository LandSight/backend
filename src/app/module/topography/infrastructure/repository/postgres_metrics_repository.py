"""PostgreSQL metrics repository implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from sqlalchemy import delete, select

from app.module.topography.application.port import MetricsRepository
from app.module.topography.domain.entity import TopographyMetrics
from app.module.topography.domain.value_object.metric import (
    Area,
    AspectDirection,
    CompactnessIndex,
    Elevation,
    ElongationIndex,
    ParcelId,
    Percentage,
    Perimeter,
    Slope,
    SlopeDistribution,
    SlopePercentiles,
    TopographyMetricsId,
)
from app.module.topography.infrastructure.model import TopographyMetricsModel
from app.platform.database.repository import BaseSQLAlchemyRepository


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class PostgresMetricsRepository(BaseSQLAlchemyRepository, MetricsRepository):
    """Metrics repository backed by PostgreSQL.

    Stores topography metrics in the ``topography.metrics`` table.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @override
    async def save(self, metrics: TopographyMetrics) -> TopographyMetrics:
        """See :class:`app.module.topography.application.port.MetricsRepository.save`."""
        model = TopographyMetricsModel(
            id=metrics.id.unwrap(),
            parcel_id=metrics.parcel_id.unwrap(),
            mean_elevation=metrics.mean_elevation.unwrap(),
            max_elevation=metrics.max_elevation.unwrap(),
            min_elevation=metrics.min_elevation.unwrap(),
            elevation_range=metrics.elevation_range.unwrap(),
            elevation_std=metrics.elevation_std.unwrap(),
            mean_slope=metrics.mean_slope.unwrap(),
            max_slope=metrics.max_slope.unwrap(),
            slope_percentiles=metrics.slope_percentiles.to_float_dict(),
            slope_distribution=metrics.slope_distribution.to_float_list(),
            aspect=metrics.aspect.value,
            south_aspect_percentage=metrics.south_aspect_percentage.unwrap(),
            area=metrics.area.unwrap(),
            perimeter=metrics.perimeter.unwrap(),
            compactness_index=metrics.compactness_index.unwrap(),
            elongation_index=metrics.elongation_index.unwrap(),
        )
        # MVP keeps at most one row per parcel: recalculating overwrites the
        # previous snapshot instead of accumulating history.
        await self._session.execute(
            delete(TopographyMetricsModel).where(TopographyMetricsModel.parcel_id == metrics.parcel_id.unwrap())
        )
        self._session.add(model)
        await self._session.flush()

        return self._to_domain(model)

    @override
    async def get(self, metrics_id: TopographyMetricsId) -> TopographyMetrics | None:
        """See :class:`app.module.topography.application.port.MetricsRepository.get`."""
        result = await self._session.execute(
            select(TopographyMetricsModel).where(TopographyMetricsModel.id == metrics_id.unwrap()),
        )
        model = result.scalar_one_or_none()

        return self._to_domain(model) if model is not None else None

    @override
    async def get_parcel_metrics(self, parcel_id: ParcelId) -> TopographyMetrics | None:
        """See :class:`app.module.topography.application.port.MetricsRepository.get_parcel_metrics`."""
        result = await self._session.execute(
            select(TopographyMetricsModel)
            .where(TopographyMetricsModel.parcel_id == parcel_id.unwrap())
            .order_by(TopographyMetricsModel.created_at.desc())
            .limit(1),
        )
        model = result.scalar_one_or_none()

        return self._to_domain(model) if model is not None else None

    @staticmethod
    def _to_domain(model: TopographyMetricsModel) -> TopographyMetrics:
        """Convert an ORM model to a domain entity."""
        return TopographyMetrics(
            id=TopographyMetricsId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            mean_elevation=Elevation(model.mean_elevation),
            max_elevation=Elevation(model.max_elevation),
            min_elevation=Elevation(model.min_elevation),
            elevation_range=Elevation(model.elevation_range),
            elevation_std=Elevation(model.elevation_std),
            mean_slope=Slope(model.mean_slope),
            max_slope=Slope(model.max_slope),
            slope_percentiles=SlopePercentiles(
                {Percentage(float(k)): Slope(v) for k, v in model.slope_percentiles.items()},
            ),
            slope_distribution=SlopeDistribution(
                [Percentage(v) for v in model.slope_distribution],
            ),
            aspect=AspectDirection(model.aspect),
            south_aspect_percentage=Percentage(model.south_aspect_percentage),
            area=Area(model.area),
            perimeter=Perimeter(model.perimeter),
            compactness_index=CompactnessIndex(model.compactness_index),
            elongation_index=ElongationIndex(model.elongation_index),
            created_at=model.created_at,
        )


__all__ = ("PostgresMetricsRepository",)
