"""PostgreSQL analysis repository implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from sqlalchemy import delete, select

from app.module.analysis.application.port import AnalysisRepository
from app.module.analysis.domain.entity import Analysis
from app.module.analysis.domain.value_object import (
    AnalysisId,
    AnalysisMetricRef,
    AnalysisName,
    AnalysisScore,
    AnalysisStatus,
    MetricType,
    ParcelId,
)
from app.module.analysis.infrastructure.model import AnalysisMetricModel, AnalysisModel
from app.platform.database.repository import BaseSQLAlchemyRepository


if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession


class PostgresAnalysisRepository(BaseSQLAlchemyRepository, AnalysisRepository):
    """Analysis repository backed by PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @override
    async def save(self, analysis: Analysis) -> Analysis:
        """See :class:`app.module.analysis.application.port.AnalysisRepository.save`."""
        model = await self._session.get(AnalysisModel, analysis.id.unwrap())
        if model is None:
            model = AnalysisModel(
                id=analysis.id.unwrap(),
                parcel_id=analysis.parcel_id.unwrap(),
                name=analysis.name.unwrap(),
                status=analysis.status.value,
                score=analysis.score.unwrap() if analysis.score is not None else None,
                status_reason=analysis.status_reason,
            )
            self._session.add(model)
        else:
            model.name = analysis.name.unwrap()
            model.status = analysis.status.value
            model.score = analysis.score.unwrap() if analysis.score is not None else None
            model.status_reason = analysis.status_reason

        await self._session.flush()

        return self._to_domain(model)

    @override
    async def get(self, analysis_id: AnalysisId) -> Analysis | None:
        """See :class:`app.module.analysis.application.port.AnalysisRepository.get`."""
        model = await self._session.get(AnalysisModel, analysis_id.unwrap())
        return self._to_domain(model) if model is not None else None

    @override
    async def list_by_parcel_ids(self, parcel_ids: list[UUID]) -> list[Analysis]:
        """See :class:`app.module.analysis.application.port.AnalysisRepository.list_by_parcel_ids`."""
        if not parcel_ids:
            return []

        result = await self._session.execute(
            select(AnalysisModel)
            .where(AnalysisModel.parcel_id.in_(parcel_ids))
            .order_by(AnalysisModel.created_at.desc()),
        )
        return [self._to_domain(model) for model in result.scalars().all()]

    @override
    async def save_metrics(self, analysis_id: AnalysisId, metrics: list[AnalysisMetricRef]) -> None:
        """See :class:`app.module.analysis.application.port.AnalysisRepository.save_metrics`."""
        await self._session.execute(
            delete(AnalysisMetricModel).where(AnalysisMetricModel.analysis_id == analysis_id.unwrap()),
        )
        self._session.add_all(
            [
                AnalysisMetricModel(
                    analysis_id=analysis_id.unwrap(),
                    metric_type=ref.metric_type.value,
                    category=ref.category,
                    metric_id=ref.metric_id,
                )
                for ref in metrics
            ]
        )
        await self._session.flush()

    @override
    async def get_metrics(self, analysis_id: AnalysisId) -> list[AnalysisMetricRef]:
        """See :class:`app.module.analysis.application.port.AnalysisRepository.get_metrics`."""
        result = await self._session.execute(
            select(AnalysisMetricModel).where(AnalysisMetricModel.analysis_id == analysis_id.unwrap()),
        )
        return [
            AnalysisMetricRef(
                metric_type=MetricType(model.metric_type),
                metric_id=model.metric_id,
                category=model.category,
            )
            for model in result.scalars().all()
        ]

    @staticmethod
    def _to_domain(model: AnalysisModel) -> Analysis:
        """Convert an ORM model to a domain entity."""
        return Analysis(
            id=AnalysisId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            name=AnalysisName(model.name),
            status=AnalysisStatus(model.status),
            score=AnalysisScore(model.score) if model.score is not None else None,
            status_reason=model.status_reason,
            created_at=model.created_at,
        )


__all__ = ("PostgresAnalysisRepository",)
