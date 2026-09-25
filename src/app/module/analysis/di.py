"""Dependency injection for Analysis module.

``analysis_dependencies`` wires the HTTP-facing internal API. The worker-only
graph (metrics collection, pipeline use cases) lives in
``analysis_worker_dependencies`` and is assembled by the worker composition
root, so the application layer never depends on concrete implementations.
"""

from celery import Celery
from litestar.di import NamedDependency, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.analysis.application.port import (
    AnalysisScorer,
    AnalysisTaskQueue,
    MetricsCollector,
    MetricsReader,
    MetricsRemover,
    UnitOfWork,
)
from app.module.analysis.application.use_case import (
    CollectMetricsUseCase,
    DeleteAnalysisUseCase,
    FailAnalysisUseCase,
    GetAnalysisEvaluationUseCase,
    GetAnalysisMetricsUseCase,
    GetAnalysisUseCase,
    ListUserAnalysesUseCase,
    ScoreAnalysisUseCase,
    StartAnalysisUseCase,
)
from app.module.analysis.domain.analysis_policy import INFRASTRUCTURE_BUFFERS
from app.module.analysis.domain.value_object import AnalysisType
from app.module.analysis.infrastructure.collector import MetricsCollectorImpl
from app.module.analysis.infrastructure.parcel import OwnedParcelsProviderImpl
from app.module.analysis.infrastructure.permission import AnalysisPermissionServiceImpl
from app.module.analysis.infrastructure.queue import CeleryAnalysisTaskQueue
from app.module.analysis.infrastructure.reader import MetricsReaderImpl
from app.module.analysis.infrastructure.remover import MetricsRemoverImpl
from app.module.analysis.infrastructure.repository import PostgresAnalysisRepository, YamlEngineConfigRepository
from app.module.analysis.infrastructure.scorer import HmcdaAnalysisScorer, build_hmcda_profile
from app.module.analysis.infrastructure.uow import SqlAlchemyUnitOfWork
from app.module.analysis.interface.internal.api import AnalysisInternal
from app.module.climate.interface.internal.port import ClimateInternalAPI
from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI
from app.module.parcel.interface.internal.port import ParcelInternalAPI
from app.module.topography.interface.internal.port import TopographyInternalAPI


COLLECT_METRICS_USE_CASE_KEY = "collect_metrics_use_case"
SCORE_ANALYSIS_USE_CASE_KEY = "score_analysis_use_case"


# ----- Repositories -----
def provide_postgres_analysis_repository(
    session: NamedDependency[AsyncSession],
) -> PostgresAnalysisRepository:
    return PostgresAnalysisRepository(session)


# ----- Permission -----
def provide_analysis_permission_service(
    parcel_api: NamedDependency[ParcelInternalAPI],
) -> AnalysisPermissionServiceImpl:
    return AnalysisPermissionServiceImpl(parcel_api)


def provide_owned_parcels_provider(
    parcel_api: NamedDependency[ParcelInternalAPI],
) -> OwnedParcelsProviderImpl:
    return OwnedParcelsProviderImpl(parcel_api)


# ----- Engine configuration -----
def provide_yaml_engine_config_repository() -> YamlEngineConfigRepository:
    return YamlEngineConfigRepository()


# ----- Scoring -----
def provide_analysis_scorer(
    yaml_engine_config_repository: NamedDependency[YamlEngineConfigRepository],
) -> HmcdaAnalysisScorer:
    profiles = {
        analysis_type: build_hmcda_profile(
            yaml_engine_config_repository.get_hierarchy(analysis_type),
            yaml_engine_config_repository.get_fuzzy_functions(analysis_type),
        )
        for analysis_type in AnalysisType
    }
    return HmcdaAnalysisScorer(profiles)


# ----- Task queue -----
def provide_analysis_task_queue(celery_app: NamedDependency[Celery]) -> CeleryAnalysisTaskQueue:
    return CeleryAnalysisTaskQueue(celery_app)


# ----- Use Cases -----
def provide_start_analysis_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    analysis_permission_service: NamedDependency[AnalysisPermissionServiceImpl],
    owned_parcels_provider: NamedDependency[OwnedParcelsProviderImpl],
    analysis_task_queue: NamedDependency[AnalysisTaskQueue],
) -> StartAnalysisUseCase:
    return StartAnalysisUseCase(
        analysis_repository,
        analysis_permission_service,
        owned_parcels_provider,
        analysis_task_queue,
    )


def provide_get_analysis_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    analysis_permission_service: NamedDependency[AnalysisPermissionServiceImpl],
    owned_parcels_provider: NamedDependency[OwnedParcelsProviderImpl],
) -> GetAnalysisUseCase:
    return GetAnalysisUseCase(analysis_repository, analysis_permission_service, owned_parcels_provider)


def provide_get_analysis_metrics_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    analysis_permission_service: NamedDependency[AnalysisPermissionServiceImpl],
) -> GetAnalysisMetricsUseCase:
    return GetAnalysisMetricsUseCase(analysis_repository, analysis_permission_service)


def provide_get_analysis_evaluation_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    analysis_permission_service: NamedDependency[AnalysisPermissionServiceImpl],
) -> GetAnalysisEvaluationUseCase:
    return GetAnalysisEvaluationUseCase(analysis_repository, analysis_permission_service)


def provide_list_user_analyses_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    owned_parcels_provider: NamedDependency[OwnedParcelsProviderImpl],
) -> ListUserAnalysesUseCase:
    return ListUserAnalysesUseCase(analysis_repository, owned_parcels_provider)


def provide_delete_analysis_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    analysis_permission_service: NamedDependency[AnalysisPermissionServiceImpl],
    metrics_remover: NamedDependency[MetricsRemover],
) -> DeleteAnalysisUseCase:
    return DeleteAnalysisUseCase(analysis_repository, analysis_permission_service, metrics_remover)


# ----- Internal API -----
def provide_analysis_internal(
    start_analysis_use_case: NamedDependency[StartAnalysisUseCase],
    get_analysis_use_case: NamedDependency[GetAnalysisUseCase],
    get_analysis_metrics_use_case: NamedDependency[GetAnalysisMetricsUseCase],
    get_analysis_evaluation_use_case: NamedDependency[GetAnalysisEvaluationUseCase],
    list_user_analyses_use_case: NamedDependency[ListUserAnalysesUseCase],
    delete_analysis_use_case: NamedDependency[DeleteAnalysisUseCase],
) -> AnalysisInternal:
    return AnalysisInternal(
        start_analysis_use_case,
        get_analysis_use_case,
        get_analysis_metrics_use_case,
        get_analysis_evaluation_use_case,
        list_user_analyses_use_case,
        delete_analysis_use_case,
    )


# ----- Worker (background pipeline) -----
def provide_analysis_unit_of_work(
    session: NamedDependency[AsyncSession],
) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session)


def provide_metrics_collector(
    topography_api: NamedDependency[TopographyInternalAPI],
    climate_api: NamedDependency[ClimateInternalAPI],
    infrastructure_api: NamedDependency[InfrastructureInternalAPI],
) -> MetricsCollectorImpl:
    return MetricsCollectorImpl(topography_api, climate_api, infrastructure_api)


def provide_metrics_reader(
    topography_api: NamedDependency[TopographyInternalAPI],
    climate_api: NamedDependency[ClimateInternalAPI],
    infrastructure_api: NamedDependency[InfrastructureInternalAPI],
) -> MetricsReaderImpl:
    return MetricsReaderImpl(topography_api, climate_api, infrastructure_api)


def provide_metrics_remover(
    topography_api: NamedDependency[TopographyInternalAPI],
    climate_api: NamedDependency[ClimateInternalAPI],
    infrastructure_api: NamedDependency[InfrastructureInternalAPI],
) -> MetricsRemoverImpl:
    return MetricsRemoverImpl(topography_api, climate_api, infrastructure_api)


def provide_analysis_infrastructure_buffers() -> dict[str, int]:
    return dict(INFRASTRUCTURE_BUFFERS)


def provide_fail_analysis_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
) -> FailAnalysisUseCase:
    return FailAnalysisUseCase(analysis_repository)


def provide_collect_metrics_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    metrics_collector: NamedDependency[MetricsCollector],
    fail_analysis_use_case: NamedDependency[FailAnalysisUseCase],
    analysis_unit_of_work: NamedDependency[UnitOfWork],
    analysis_infrastructure_buffers: NamedDependency[dict[str, int]],
) -> CollectMetricsUseCase:
    return CollectMetricsUseCase(
        analysis_repository,
        metrics_collector,
        fail_analysis_use_case,
        analysis_unit_of_work,
        analysis_infrastructure_buffers,
    )


def provide_score_analysis_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    metrics_reader: NamedDependency[MetricsReader],
    analysis_scorer: NamedDependency[AnalysisScorer],
    fail_analysis_use_case: NamedDependency[FailAnalysisUseCase],
    analysis_unit_of_work: NamedDependency[UnitOfWork],
) -> ScoreAnalysisUseCase:
    return ScoreAnalysisUseCase(
        analysis_repository,
        metrics_reader,
        analysis_scorer,
        fail_analysis_use_case,
        analysis_unit_of_work,
    )


analysis_dependencies = {
    "analysis_repository": Provide(provide_postgres_analysis_repository, sync_to_thread=False),
    "analysis_permission_service": Provide(provide_analysis_permission_service, sync_to_thread=False),
    "owned_parcels_provider": Provide(provide_owned_parcels_provider, sync_to_thread=False),
    "yaml_engine_config_repository": Provide(
        provide_yaml_engine_config_repository,
        use_cache=True,
        sync_to_thread=False,
    ),
    "analysis_scorer": Provide(provide_analysis_scorer, use_cache=True, sync_to_thread=False),
    "metrics_remover": Provide(provide_metrics_remover, sync_to_thread=False),
    "analysis_task_queue": Provide(provide_analysis_task_queue, sync_to_thread=False),
    "start_analysis_use_case": Provide(provide_start_analysis_use_case, sync_to_thread=False),
    "get_analysis_use_case": Provide(provide_get_analysis_use_case, sync_to_thread=False),
    "get_analysis_metrics_use_case": Provide(provide_get_analysis_metrics_use_case, sync_to_thread=False),
    "get_analysis_evaluation_use_case": Provide(provide_get_analysis_evaluation_use_case, sync_to_thread=False),
    "list_user_analyses_use_case": Provide(provide_list_user_analyses_use_case, sync_to_thread=False),
    "delete_analysis_use_case": Provide(provide_delete_analysis_use_case, sync_to_thread=False),
    "analysis_api": Provide(provide_analysis_internal, sync_to_thread=False),
}

analysis_worker_dependencies = {
    "analysis_unit_of_work": Provide(provide_analysis_unit_of_work, sync_to_thread=False),
    "metrics_collector": Provide(provide_metrics_collector, sync_to_thread=False),
    "metrics_reader": Provide(provide_metrics_reader, sync_to_thread=False),
    "analysis_infrastructure_buffers": Provide(
        provide_analysis_infrastructure_buffers,
        use_cache=True,
        sync_to_thread=False,
    ),
    "fail_analysis_use_case": Provide(provide_fail_analysis_use_case, sync_to_thread=False),
    COLLECT_METRICS_USE_CASE_KEY: Provide(provide_collect_metrics_use_case, sync_to_thread=False),
    SCORE_ANALYSIS_USE_CASE_KEY: Provide(provide_score_analysis_use_case, sync_to_thread=False),
}

__all__ = (
    "COLLECT_METRICS_USE_CASE_KEY",
    "SCORE_ANALYSIS_USE_CASE_KEY",
    "analysis_dependencies",
    "analysis_worker_dependencies",
)
