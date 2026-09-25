"""PostgreSQL analysis repository implementation."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, override
from uuid import uuid6

from sqlalchemy import delete, select

from app.module.analysis.application.port import AnalysisRepository
from app.module.analysis.domain.entity import Analysis, AnalysisEvaluation
from app.module.analysis.domain.value_object import (
    AnalysisEvaluationId,
    AnalysisId,
    AnalysisKey,
    AnalysisMetricRef,
    AnalysisName,
    AnalysisScore,
    AnalysisStage,
    AnalysisStatus,
    AnalysisType,
    ClusterScore,
    Contribution,
    MetricContribution,
    MetricType,
    NormalizedScore,
    ParcelId,
    Weight,
)
from app.module.analysis.infrastructure.model import (
    AnalysisClusterScoreModel,
    AnalysisEvaluationModel,
    AnalysisMetricContributionModel,
    AnalysisMetricModel,
    AnalysisModel,
)
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
                analysis_type=analysis.analysis_type.value,
                status=analysis.status.value,
                stage=analysis.stage.value,
                score=analysis.score.unwrap() if analysis.score is not None else None,
                model_version=analysis.model_version,
                status_reason=analysis.status_reason,
                completed_at=analysis.completed_at,
            )
            self._session.add(model)
        else:
            model.name = analysis.name.unwrap()
            model.analysis_type = analysis.analysis_type.value
            model.status = analysis.status.value
            model.stage = analysis.stage.value
            model.score = analysis.score.unwrap() if analysis.score is not None else None
            model.model_version = analysis.model_version
            model.status_reason = analysis.status_reason
            model.completed_at = analysis.completed_at

        await self._session.flush()

        return self._to_domain(model)

    @override
    async def get(self, analysis_id: AnalysisId) -> Analysis | None:
        """See :class:`app.module.analysis.application.port.AnalysisRepository.get`."""
        model = await self._session.get(AnalysisModel, analysis_id.unwrap())
        return self._to_domain(model) if model is not None else None

    @override
    async def delete(self, analysis_id: AnalysisId) -> None:
        """See :class:`app.module.analysis.application.port.AnalysisRepository.delete`."""
        await self._session.execute(delete(AnalysisModel).where(AnalysisModel.id == analysis_id.unwrap()))
        await self._session.flush()

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
        if not metrics:
            return

        metric_types = {ref.metric_type.value for ref in metrics}
        await self._session.execute(
            delete(AnalysisMetricModel).where(
                AnalysisMetricModel.analysis_id == analysis_id.unwrap(),
                AnalysisMetricModel.metric_type.in_(metric_types),
            ),
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

    @override
    async def save_evaluation(self, evaluation: AnalysisEvaluation) -> None:
        """See :class:`app.module.analysis.application.port.AnalysisRepository.save_evaluation`."""
        analysis_id = evaluation.analysis_id.unwrap()
        await self._session.execute(
            delete(AnalysisEvaluationModel).where(AnalysisEvaluationModel.analysis_id == analysis_id),
        )

        evaluation_id = evaluation.id.unwrap()
        self._session.add(
            AnalysisEvaluationModel(
                id=evaluation_id,
                analysis_id=analysis_id,
                analysis_type=evaluation.analysis_type.value,
                model_version=evaluation.model_version,
                total_score=evaluation.total_score.unwrap(),
            )
        )

        group_rows: list[AnalysisClusterScoreModel] = []
        contribution_rows: list[AnalysisMetricContributionModel] = []

        def collect(node: ClusterScore, parent_id: UUID | None, depth: int, position: int) -> None:
            """Collect the group row and, recursively, its children and metrics."""
            group_id = uuid6()
            group_rows.append(
                AnalysisClusterScoreModel(
                    id=group_id,
                    evaluation_id=evaluation_id,
                    parent_id=parent_id,
                    key=node.key.unwrap(),
                    depth=depth,
                    score=node.score.unwrap(),
                    weight=node.weight.unwrap(),
                    contribution=node.contribution.unwrap(),
                    position=position,
                )
            )
            for child_position, child in enumerate(node.subclusters):
                collect(child, group_id, depth + 1, child_position)
            for metric_position, metric in enumerate(node.metrics):
                contribution_rows.append(
                    AnalysisMetricContributionModel(
                        evaluation_id=evaluation_id,
                        cluster_score_id=group_id,
                        metric_key=metric.key.unwrap(),
                        position=metric_position,
                        raw_value=metric.raw_value,
                        normalized_value=(
                            None if metric.normalized_value is None else metric.normalized_value.unwrap()
                        ),
                        weight=metric.weight.unwrap(),
                        contribution=None if metric.contribution is None else metric.contribution.unwrap(),
                        unit=metric.unit,
                        membership_function=metric.membership_function,
                        membership_params=dict(metric.membership_params) if metric.membership_params else None,
                    )
                )

        for position, cluster in enumerate(evaluation.clusters):
            collect(cluster, None, 0, position)

        self._session.add_all(group_rows)
        self._session.add_all(contribution_rows)
        await self._session.flush()

    @override
    async def get_evaluation(self, analysis_id: AnalysisId) -> AnalysisEvaluation | None:
        """See :class:`app.module.analysis.application.port.AnalysisRepository.get_evaluation`."""
        evaluation_result = await self._session.execute(
            select(AnalysisEvaluationModel)
            .where(AnalysisEvaluationModel.analysis_id == analysis_id.unwrap())
            .order_by(AnalysisEvaluationModel.created_at.desc())
            .limit(1),
        )
        evaluation_model = evaluation_result.scalars().first()
        if evaluation_model is None:
            return None

        group_result = await self._session.execute(
            select(AnalysisClusterScoreModel)
            .where(AnalysisClusterScoreModel.evaluation_id == evaluation_model.id)
            .order_by(AnalysisClusterScoreModel.depth, AnalysisClusterScoreModel.position),
        )
        group_models = list(group_result.scalars().all())

        contribution_result = await self._session.execute(
            select(AnalysisMetricContributionModel)
            .where(AnalysisMetricContributionModel.evaluation_id == evaluation_model.id)
            .order_by(AnalysisMetricContributionModel.position),
        )
        metrics_by_group: dict[UUID, list[AnalysisMetricContributionModel]] = defaultdict(list)
        for contribution in contribution_result.scalars().all():
            metrics_by_group[contribution.cluster_score_id].append(contribution)

        children_by_parent: dict[UUID, list[AnalysisClusterScoreModel]] = defaultdict(list)
        roots: list[AnalysisClusterScoreModel] = []
        for group in group_models:
            if group.parent_id is None:
                roots.append(group)
            else:
                children_by_parent[group.parent_id].append(group)

        def build_group(group: AnalysisClusterScoreModel) -> ClusterScore:
            """Rebuild one group with its nested groups and metric contributions."""
            return ClusterScore(
                key=AnalysisKey(group.key),
                score=NormalizedScore(group.score),
                weight=Weight(group.weight),
                contribution=Contribution(group.contribution),
                subclusters=tuple(build_group(child) for child in children_by_parent[group.id]),
                metrics=tuple(self._to_metric(row) for row in metrics_by_group[group.id]),
            )

        clusters = tuple(build_group(root) for root in roots)
        return AnalysisEvaluation(
            id=AnalysisEvaluationId(evaluation_model.id),
            analysis_id=AnalysisId(evaluation_model.analysis_id),
            analysis_type=AnalysisType(evaluation_model.analysis_type),
            model_version=evaluation_model.model_version,
            total_score=AnalysisScore(evaluation_model.total_score),
            clusters=clusters,
            created_at=evaluation_model.created_at,
        )

    @staticmethod
    def _to_metric(row: AnalysisMetricContributionModel) -> MetricContribution:
        """Rebuild one metric contribution."""
        return MetricContribution(
            key=AnalysisKey(row.metric_key),
            raw_value=row.raw_value,
            normalized_value=None if row.normalized_value is None else NormalizedScore(row.normalized_value),
            weight=Weight(row.weight),
            contribution=None if row.contribution is None else Contribution(row.contribution),
            unit=row.unit,
            membership_function=row.membership_function,
            membership_params=row.membership_params,
        )

    @staticmethod
    def _to_domain(model: AnalysisModel) -> Analysis:
        """Convert an ORM model to a domain entity."""
        return Analysis(
            id=AnalysisId(model.id),
            parcel_id=ParcelId(model.parcel_id),
            name=AnalysisName(model.name),
            analysis_type=AnalysisType(model.analysis_type),
            status=AnalysisStatus(model.status),
            stage=AnalysisStage(model.stage),
            score=AnalysisScore(model.score) if model.score is not None else None,
            model_version=model.model_version,
            status_reason=model.status_reason,
            created_at=model.created_at,
            completed_at=model.completed_at,
        )


__all__ = ("PostgresAnalysisRepository",)
