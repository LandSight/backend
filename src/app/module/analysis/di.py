"""Dependency injection for Analysis module."""

from litestar.di import NamedDependency, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.analysis.application.port import AnalysisTaskQueue
from app.module.analysis.application.use_case import (
    GetAnalysisUseCase,
    ListUserAnalysesUseCase,
    StartAnalysisUseCase,
)
from app.module.analysis.infrastructure.parcel import OwnedParcelsProviderImpl
from app.module.analysis.infrastructure.permission import AnalysisPermissionServiceImpl
from app.module.analysis.infrastructure.queue import NoopAnalysisTaskQueue
from app.module.analysis.infrastructure.repository import PostgresAnalysisRepository
from app.module.analysis.infrastructure.scoring import RandomAnalysisScorer
from app.module.analysis.interface.internal.api import AnalysisInternal
from app.module.parcel.interface.internal.port import ParcelInternalAPI


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


# ----- Scoring -----
def provide_random_analysis_scorer() -> RandomAnalysisScorer:
    return RandomAnalysisScorer()


# ----- Task queue -----
def provide_analysis_task_queue() -> NoopAnalysisTaskQueue:
    return NoopAnalysisTaskQueue()


# ----- Use Cases -----
def provide_start_analysis_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    analysis_permission_service: NamedDependency[AnalysisPermissionServiceImpl],
    analysis_task_queue: NamedDependency[AnalysisTaskQueue],
) -> StartAnalysisUseCase:
    return StartAnalysisUseCase(analysis_repository, analysis_permission_service, analysis_task_queue)


def provide_get_analysis_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    analysis_permission_service: NamedDependency[AnalysisPermissionServiceImpl],
) -> GetAnalysisUseCase:
    return GetAnalysisUseCase(analysis_repository, analysis_permission_service)


def provide_list_user_analyses_use_case(
    analysis_repository: NamedDependency[PostgresAnalysisRepository],
    owned_parcels_provider: NamedDependency[OwnedParcelsProviderImpl],
) -> ListUserAnalysesUseCase:
    return ListUserAnalysesUseCase(analysis_repository, owned_parcels_provider)


# ----- Internal API -----
def provide_analysis_internal(
    start_analysis_use_case: NamedDependency[StartAnalysisUseCase],
    get_analysis_use_case: NamedDependency[GetAnalysisUseCase],
    list_user_analyses_use_case: NamedDependency[ListUserAnalysesUseCase],
) -> AnalysisInternal:
    return AnalysisInternal(start_analysis_use_case, get_analysis_use_case, list_user_analyses_use_case)


analysis_dependencies = {
    "analysis_repository": Provide(provide_postgres_analysis_repository, sync_to_thread=False),
    "analysis_permission_service": Provide(provide_analysis_permission_service, sync_to_thread=False),
    "owned_parcels_provider": Provide(provide_owned_parcels_provider, sync_to_thread=False),
    "analysis_scorer": Provide(provide_random_analysis_scorer, sync_to_thread=False),
    "analysis_task_queue": Provide(provide_analysis_task_queue, sync_to_thread=False),
    "start_analysis_use_case": Provide(provide_start_analysis_use_case, sync_to_thread=False),
    "get_analysis_use_case": Provide(provide_get_analysis_use_case, sync_to_thread=False),
    "list_user_analyses_use_case": Provide(provide_list_user_analyses_use_case, sync_to_thread=False),
    "analysis_api": Provide(provide_analysis_internal, sync_to_thread=False),
}

__all__ = ("analysis_dependencies",)
