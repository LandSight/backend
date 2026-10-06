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
    AnalysisProfileProvider,
    AnalysisScorer,
    InterpretationService,
    MetricsService,
    ParcelsService,
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
from app.module.analysis.infrastructure.config import load_analysis_profiles
from app.module.analysis.infrastructure.gateways import (
    InterpretationServiceImpl,
    MetricsServiceImpl,
    ParcelsServiceImpl,
)
from app.module.analysis.infrastructure.permission import AnalysisPermissionServiceImpl
from app.module.analysis.infrastructure.provider import AnalysisProfileProviderImpl, EngineProviderImpl
from app.module.analysis.infrastructure.queue import CeleryAnalysisTaskQueue
from app.module.analysis.infrastructure.repository import PostgresAnalysisRepository
from app.module.analysis.infrastructure.scorer import HmcdaAnalysisScorer
from app.module.analysis.infrastructure.scorer.hmcda.config import load_engine_config
from app.module.analysis.interface.internal.api import AnalysisInternal
from app.module.climate.interface.internal.port import ClimateInternalAPI
from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI
from app.module.interpretation.interface.internal.port import InterpretationInternalAPI
from app.module.parcel.interface.internal.port import ParcelInternalAPI
from app.module.shared.application.port import EventPublisher, UnitOfWork
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


def provide_parcels_service(
    parcel_api: NamedDependency[ParcelInternalAPI],
) -> ParcelsServiceImpl:
    return ParcelsServiceImpl(parcel_api)


# ----- Scoring -----
def provide_analysis_scorer() -> HmcdaAnalysisScorer:
    return HmcdaAnalysisScorer(load_engine_config())


def provide_engine_provider() -> EngineProviderImpl:
    return EngineProviderImpl(load_engine_config())


# ----- Task queue -----
def provide_analysis_task_queue(celery_app: NamedDependency[Celery]) -> CeleryAnalysisTaskQueue:
    return CeleryAnalysisTaskQueue(celery_app)


# ----- Use Cases -----
def provide_start_analysis_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    analysis_permission_service: NamedDependency[AnalysisPermissionServiceImpl],
    parcels_service: NamedDependency[ParcelsService],
    event_publisher: NamedDependency[EventPublisher],
) -> StartAnalysisUseCase:
    return StartAnalysisUseCase(
        analysis_repository,
        analysis_permission_service,
        parcels_service,
        event_publisher,
    )


def provide_get_analysis_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    analysis_permission_service: NamedDependency[AnalysisPermissionServiceImpl],
    parcels_service: NamedDependency[ParcelsService],
) -> GetAnalysisUseCase:
    return GetAnalysisUseCase(analysis_repository, analysis_permission_service, parcels_service)


def provide_get_analysis_metrics_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    analysis_permission_service: NamedDependency[AnalysisPermissionServiceImpl],
) -> GetAnalysisMetricsUseCase:
    return GetAnalysisMetricsUseCase(analysis_repository, analysis_permission_service)


def provide_get_analysis_evaluation_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    analysis_permission_service: NamedDependency[AnalysisPermissionServiceImpl],
    analysis_profiles: NamedDependency[AnalysisProfileProvider],
) -> GetAnalysisEvaluationUseCase:
    return GetAnalysisEvaluationUseCase(analysis_repository, analysis_permission_service, analysis_profiles)


def provide_list_user_analyses_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    parcels_service: NamedDependency[ParcelsService],
) -> ListUserAnalysesUseCase:
    return ListUserAnalysesUseCase(analysis_repository, parcels_service)


def provide_delete_analysis_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    analysis_permission_service: NamedDependency[AnalysisPermissionServiceImpl],
    event_publisher: NamedDependency[EventPublisher],
) -> DeleteAnalysisUseCase:
    return DeleteAnalysisUseCase(analysis_repository, analysis_permission_service, event_publisher)


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
def provide_metrics_service(
    topography_api: NamedDependency[TopographyInternalAPI],
    climate_api: NamedDependency[ClimateInternalAPI],
    infrastructure_api: NamedDependency[InfrastructureInternalAPI],
) -> MetricsServiceImpl:
    return MetricsServiceImpl(topography_api, climate_api, infrastructure_api)


def provide_analysis_profiles() -> AnalysisProfileProviderImpl:
    return AnalysisProfileProviderImpl(load_analysis_profiles())


def provide_fail_analysis_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
) -> FailAnalysisUseCase:
    return FailAnalysisUseCase(analysis_repository)


def provide_collect_metrics_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    metrics_service: NamedDependency[MetricsService],
    fail_analysis_use_case: NamedDependency[FailAnalysisUseCase],
    unit_of_work: NamedDependency[UnitOfWork],
    analysis_profiles: NamedDependency[AnalysisProfileProvider],
) -> CollectMetricsUseCase:
    return CollectMetricsUseCase(
        analysis_repository,
        metrics_service,
        fail_analysis_use_case,
        unit_of_work,
        analysis_profiles,
    )


def provide_interpretation_service(
    interpretation_api: NamedDependency[InterpretationInternalAPI],
) -> InterpretationServiceImpl:
    return InterpretationServiceImpl(interpretation_api)


def provide_score_analysis_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    metrics_service: NamedDependency[MetricsService],
    analysis_scorer: NamedDependency[AnalysisScorer],
    fail_analysis_use_case: NamedDependency[FailAnalysisUseCase],
    unit_of_work: NamedDependency[UnitOfWork],
    interpretation_service: NamedDependency[InterpretationService],
) -> ScoreAnalysisUseCase:
    return ScoreAnalysisUseCase(
        analysis_repository,
        metrics_service,
        analysis_scorer,
        fail_analysis_use_case,
        unit_of_work,
        interpretation_service,
    )


analysis_dependencies = {
    "analysis_repository": Provide(provide_postgres_analysis_repository, sync_to_thread=False),
    "analysis_permission_service": Provide(provide_analysis_permission_service, sync_to_thread=False),
    "parcels_service": Provide(provide_parcels_service, sync_to_thread=False),
    "metrics_service": Provide(provide_metrics_service, sync_to_thread=False),
    "analysis_scorer": Provide(provide_analysis_scorer, use_cache=True, sync_to_thread=False),
    "engine_provider": Provide(provide_engine_provider, use_cache=True, sync_to_thread=False),
    "analysis_profiles": Provide(provide_analysis_profiles, use_cache=True, sync_to_thread=False),
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
    "interpretation_service": Provide(provide_interpretation_service, sync_to_thread=False),
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
