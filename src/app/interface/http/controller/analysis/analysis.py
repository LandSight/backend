"""Analysis HTTP endpoints."""

from __future__ import annotations

from uuid import UUID

from litestar import delete, get, post
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT

from app.interface.http.schema.analysis import (
    AnalysisEvaluationSchema,
    AnalysisMetricSchema,
    AnalysisResponse,
    ClusterScoreSchema,
    ConstraintExtensionSchema,
    EvaluationMetadataSchema,
    HierarchicalExtensionSchema,
    MetricContributionSchema,
    RuleBasedExtensionSchema,
    StartAnalysisRequest,
)
from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.util.guards import require_authorization
from app.module.analysis.application.dto.response import (
    AnalysisEvaluationResponse,
    ClusterScoreResponse,
    EvaluationExtensionResponse,
    HierarchicalExtensionResponse,
    MetricContributionResponse,
    RuleBasedExtensionResponse,
)
from app.module.analysis.interface.internal.dto import (
    AnalysisResult,
    DeleteAnalysisInput,
    GetAnalysisEvaluationInput,
    GetAnalysisInput,
    GetAnalysisMetricsInput,
    ListUserAnalysesInput,
    StartAnalysisInput,
)
from app.module.analysis.interface.internal.port import AnalysisInternalAPI


class AnalysisController(Controller):
    """Analysis endpoints."""

    path = "/"
    tags = ("analysis",)
    guards = [require_authorization]

    @post(
        "/",
        status_code=HTTP_202_ACCEPTED,
        description="Start an analysis for a parcel.",
    )
    async def start_analysis(
        self,
        data: StartAnalysisRequest,
        analysis_api: AnalysisInternalAPI,
        current_user: CurrentUser,
    ) -> AnalysisResponse:
        """Start an analysis for a parcel."""
        result = await analysis_api.start_analysis(
            StartAnalysisInput(
                parcel_id=data.parcel_id,
                current_user_id=current_user.id,
                name=data.name,
                analysis_type=data.scenario,
                engine=data.engine,
            ),
        )
        return self._to_schema(result)

    @get(
        "/",
        status_code=HTTP_200_OK,
        description="List all analyses of the current user across all statuses.",
    )
    async def list_user_analyses(
        self,
        analysis_api: AnalysisInternalAPI,
        current_user: CurrentUser,
    ) -> list[AnalysisResponse]:
        """List all analyses of the current user."""
        results = await analysis_api.list_user_analyses(
            ListUserAnalysesInput(current_user_id=current_user.id),
        )
        return [self._to_schema(result) for result in results]

    @get(
        "/{analysis_id:uuid}",
        status_code=HTTP_200_OK,
        description="Get an analysis by its ID.",
    )
    async def get_analysis(
        self,
        analysis_id: UUID,
        analysis_api: AnalysisInternalAPI,
        current_user: CurrentUser,
    ) -> AnalysisResponse:
        """Get an analysis by its ID."""
        result = await analysis_api.get_analysis(
            GetAnalysisInput(analysis_id=analysis_id, current_user_id=current_user.id),
        )
        return self._to_schema(result)

    @get(
        "/{analysis_id:uuid}/metrics",
        status_code=HTTP_200_OK,
        description="List the metric references recorded for an analysis.",
    )
    async def get_analysis_metrics(
        self,
        analysis_id: UUID,
        analysis_api: AnalysisInternalAPI,
        current_user: CurrentUser,
        module: str | None = None,
    ) -> list[AnalysisMetricSchema]:
        """List the metric references recorded for an analysis."""
        results = await analysis_api.get_analysis_metrics(
            GetAnalysisMetricsInput(
                analysis_id=analysis_id,
                current_user_id=current_user.id,
                module=module,
            ),
        )
        return [
            AnalysisMetricSchema(
                module=result.module,
                category=result.category,
                metrics_id=result.metrics_id,
            )
            for result in results
        ]

    @get(
        "/{analysis_id:uuid}/evaluation",
        status_code=HTTP_200_OK,
        description="Get the stored evaluation tree of a completed analysis.",
    )
    async def get_analysis_evaluation(
        self,
        analysis_id: UUID,
        analysis_api: AnalysisInternalAPI,
        current_user: CurrentUser,
    ) -> AnalysisEvaluationSchema:
        """Get the stored evaluation tree of a completed analysis."""
        result = await analysis_api.get_analysis_evaluation(
            GetAnalysisEvaluationInput(analysis_id=analysis_id, current_user_id=current_user.id),
        )
        return self._to_evaluation_schema(result)

    @delete(
        "/{analysis_id:uuid}",
        status_code=HTTP_204_NO_CONTENT,
        description="Delete an analysis and its metric references.",
    )
    async def delete_analysis(
        self,
        analysis_id: UUID,
        analysis_api: AnalysisInternalAPI,
        current_user: CurrentUser,
    ) -> None:
        """Delete an analysis and its metric references."""
        await analysis_api.delete_analysis(
            DeleteAnalysisInput(analysis_id=analysis_id, current_user_id=current_user.id),
        )

    @staticmethod
    def _to_schema(result: AnalysisResult) -> AnalysisResponse:
        """Map an internal result DTO to the HTTP response schema."""
        return AnalysisResponse(
            id=result.id,
            parcel_id=result.parcel_id,
            parcel_name=result.parcel_name,
            name=result.name,
            scenario=result.analysis_type,
            engine=result.engine,
            status=result.status,
            stage=result.stage,
            score=result.score,
            model_version=result.model_version,
            status_reason=result.status_reason,
            created_at=result.created_at,
            completed_at=result.completed_at,
        )

    @classmethod
    def _to_evaluation_schema(cls, result: AnalysisEvaluationResponse) -> AnalysisEvaluationSchema:
        """Map an application evaluation DTO to the universal HTTP schema."""
        return AnalysisEvaluationSchema(
            scenario=result.scenario,
            engine=result.engine,
            model_version=result.model_version,
            total_score=result.total_score,
            scale=result.scale,
            metadata=EvaluationMetadataSchema(
                evaluated_at=result.metadata.evaluated_at,
                parcel_id=UUID(result.metadata.parcel_id),
            ),
            extensions={key: cls._to_extension_schema(extension) for key, extension in result.extensions.items()},
        )

    @classmethod
    def _to_extension_schema(
        cls,
        extension: EvaluationExtensionResponse,
    ) -> HierarchicalExtensionSchema | RuleBasedExtensionSchema | ConstraintExtensionSchema:
        """Map an engine-specific evaluation extension to its HTTP schema."""
        if isinstance(extension, HierarchicalExtensionResponse):
            return HierarchicalExtensionSchema(
                clusters=[cls._to_cluster_schema(cluster) for cluster in extension.clusters],
            )
        if isinstance(extension, RuleBasedExtensionResponse):
            return RuleBasedExtensionSchema(
                base_score=extension.base_score,
                applied_rules=[dict(rule) for rule in extension.applied_rules],
            )
        return ConstraintExtensionSchema(
            applied_constraints=[dict(constraint) for constraint in extension.applied_constraints],
        )

    @classmethod
    def _to_cluster_schema(cls, cluster: ClusterScoreResponse) -> ClusterScoreSchema:
        """Map a group score DTO to a schema, recursing into subclusters."""
        return ClusterScoreSchema(
            key=cluster.key,
            score=cluster.score,
            weight=cluster.weight,
            contribution=cluster.contribution,
            subclusters=[cls._to_cluster_schema(subcluster) for subcluster in cluster.subclusters],
            metrics=[cls._to_metric_schema(metric) for metric in cluster.metrics],
        )

    @classmethod
    def _to_metric_schema(cls, metric: MetricContributionResponse) -> MetricContributionSchema:
        """Map a metric contribution DTO to a schema."""
        return MetricContributionSchema(
            key=metric.key,
            raw_value=metric.raw_value,
            normalized_value=metric.normalized_value,
            weight=metric.weight,
            contribution=metric.contribution,
            unit=metric.unit,
            data_available=metric.data_available,
            membership_function=metric.membership_function,
            membership_params=dict(metric.membership_params) if metric.membership_params else None,
        )


__all__ = ("AnalysisController",)
