"""Get analysis evaluation use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import GetAnalysisEvaluationCommand
from app.module.analysis.application.dto.response import (
    AnalysisEvaluationResponse,
    ClusterScoreResponse,
    MetricContributionResponse,
)
from app.module.analysis.application.error import (
    AnalysisEvaluationNotAvailableError,
    AnalysisNotFoundError,
)
from app.module.analysis.domain.value_object import AnalysisId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from typing import NoReturn
    from uuid import UUID

    from app.module.analysis.application.port import (
        AnalysisPermissionService,
        AnalysisRepository,
    )
    from app.module.analysis.domain.entity import Analysis, AnalysisEvaluation
    from app.module.analysis.domain.value_object import ClusterScore, MetricContribution


class GetAnalysisEvaluationUseCase(
    BaseUseCase[GetAnalysisEvaluationCommand, AnalysisEvaluationResponse],
):
    """Retrieve the stored evaluation tree of a completed analysis.

    Access is granted only when the current user owns the underlying parcel.
    """

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        permission_service: AnalysisPermissionService,
    ) -> None:
        self._analysis_repository = analysis_repository
        self._permission_service = permission_service
        self._logger = get_logger("app.analysis.use_case.get_analysis_evaluation")

    @override
    async def __call__(self, command: GetAnalysisEvaluationCommand) -> AnalysisEvaluationResponse:
        self._logger.info("Getting analysis evaluation: analysis_id=%s", command.analysis_id)

        analysis = await self._analysis_repository.get(AnalysisId(command.analysis_id))
        if analysis is None:
            self._raise_not_found(command.analysis_id)

        if not await self._permission_service.user_can_view_parcel(
            command.current_user_id,
            analysis.parcel_id.unwrap(),
        ):
            self._logger.warning(
                "User %s is not allowed to view analysis %s",
                command.current_user_id,
                command.analysis_id,
            )
            self._raise_not_found(command.analysis_id)

        evaluation = await self._analysis_repository.get_evaluation(analysis.id)
        if evaluation is None:
            raise AnalysisEvaluationNotAvailableError(str(command.analysis_id))

        return self._to_response(analysis, evaluation)

    @staticmethod
    def _raise_not_found(analysis_id: UUID) -> NoReturn:
        """Raise a not-found error for the given analysis ID."""
        raise AnalysisNotFoundError(str(analysis_id))

    @classmethod
    def _to_response(cls, analysis: Analysis, evaluation: AnalysisEvaluation) -> AnalysisEvaluationResponse:
        """Map a domain evaluation to a response DTO."""
        return AnalysisEvaluationResponse(
            analysis_id=str(analysis.id.unwrap()),
            analysis_type=evaluation.analysis_type.value,
            model_version=evaluation.model_version,
            total_score=evaluation.total_score.unwrap(),
            scale=evaluation.total_score.scale,
            clusters=tuple(cls._to_cluster(cluster) for cluster in evaluation.clusters),
        )

    @classmethod
    def _to_cluster(cls, cluster: ClusterScore) -> ClusterScoreResponse:
        """Map a group score, recursing into nested subclusters."""
        return ClusterScoreResponse(
            key=cluster.key.unwrap(),
            score=cluster.score.unwrap(),
            weight=cluster.weight.unwrap(),
            contribution=cluster.contribution.unwrap(),
            subclusters=tuple(cls._to_cluster(subcluster) for subcluster in cluster.subclusters),
            metrics=tuple(cls._to_metric(metric) for metric in cluster.metrics),
        )

    @classmethod
    def _to_metric(cls, metric: MetricContribution) -> MetricContributionResponse:
        """Map a metric contribution."""
        return MetricContributionResponse(
            key=metric.key.unwrap(),
            raw_value=metric.raw_value,
            normalized_value=(None if metric.normalized_value is None else metric.normalized_value.unwrap()),
            weight=metric.weight.unwrap(),
            contribution=None if metric.contribution is None else metric.contribution.unwrap(),
            unit=metric.unit,
            data_available=metric.data_available,
            membership_function=metric.membership_function,
            membership_params=metric.membership_params,
        )


__all__ = ("GetAnalysisEvaluationUseCase",)
