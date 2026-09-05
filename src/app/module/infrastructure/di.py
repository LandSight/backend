"""Dependency injection for Infrastructure module."""

from litestar.di import NamedDependency, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.infrastructure.application.use_case import (
    CalculateInfrastructureMetricsUseCase,
    GetAvailableCategoriesUseCase,
    GetInfrastructureMetricsUseCase,
)
from app.module.infrastructure.infrastructure.geo import (
    ShapelyBufferService,
    ShapelyInfrastructureMetricsService,
)
from app.module.infrastructure.infrastructure.parcel import ParcelProviderImpl
from app.module.infrastructure.infrastructure.permission import MetricsPermissionServiceImpl
from app.module.infrastructure.infrastructure.repository import (
    PostgresLocalInfrastructureRepository,
    PostgresMetricsRepository,
)
from app.module.infrastructure.interface.internal.api import InfrastructureInternal
from app.module.parcel.interface.internal.port import ParcelInternalAPI


# ----- Repositories -----
def provide_postgres_metrics_repository(
    session: NamedDependency[AsyncSession],
) -> PostgresMetricsRepository:
    return PostgresMetricsRepository(session)


def provide_postgres_local_infrastructure_repository(
    session: NamedDependency[AsyncSession],
) -> PostgresLocalInfrastructureRepository:
    return PostgresLocalInfrastructureRepository(session)


# ----- Services -----
def provide_shapely_buffer_service() -> ShapelyBufferService:
    return ShapelyBufferService()


def provide_shapely_infrastructure_metrics_service() -> ShapelyInfrastructureMetricsService:
    return ShapelyInfrastructureMetricsService()


# ----- Parcel integration -----
def provide_infrastructure_parcel_provider(
    parcel_api: NamedDependency[ParcelInternalAPI],
) -> ParcelProviderImpl:
    return ParcelProviderImpl(parcel_api)


def provide_infrastructure_metrics_permission_service(
    parcel_api: NamedDependency[ParcelInternalAPI],
) -> MetricsPermissionServiceImpl:
    return MetricsPermissionServiceImpl(parcel_api)


# ----- Use Cases -----
def provide_calculate_infrastructure_metrics_use_case(
    buffer_service: NamedDependency[ShapelyBufferService],
    local_infrastructure_repository: NamedDependency[PostgresLocalInfrastructureRepository],
    infrastructure_metrics_service: NamedDependency[ShapelyInfrastructureMetricsService],
    metrics_repository: NamedDependency[PostgresMetricsRepository],
    infrastructure_parcel_provider: NamedDependency[ParcelProviderImpl],
) -> CalculateInfrastructureMetricsUseCase:
    return CalculateInfrastructureMetricsUseCase(
        buffer_service=buffer_service,
        local_infrastructure_repository=local_infrastructure_repository,
        infrastructure_metrics_service=infrastructure_metrics_service,
        metrics_repository=metrics_repository,
        parcel_provider=infrastructure_parcel_provider,
    )


def provide_get_infrastructure_metrics_use_case(
    metrics_repository: NamedDependency[PostgresMetricsRepository],
    infrastructure_metrics_permission_service: NamedDependency[MetricsPermissionServiceImpl],
) -> GetInfrastructureMetricsUseCase:
    return GetInfrastructureMetricsUseCase(metrics_repository, infrastructure_metrics_permission_service)


def provide_get_available_categories_use_case() -> GetAvailableCategoriesUseCase:
    return GetAvailableCategoriesUseCase()


# ----- Internal API -----
def provide_infrastructure_internal(
    calculate_infrastructure_metrics_use_case: NamedDependency[CalculateInfrastructureMetricsUseCase],
    get_infrastructure_metrics_use_case: NamedDependency[GetInfrastructureMetricsUseCase],
    get_available_categories_use_case: NamedDependency[GetAvailableCategoriesUseCase],
) -> InfrastructureInternal:
    return InfrastructureInternal(
        calculate_use_case=calculate_infrastructure_metrics_use_case,
        get_use_case=get_infrastructure_metrics_use_case,
        get_categories_use_case=get_available_categories_use_case,
    )


infrastructure_dependencies = {
    "metrics_repository": Provide(provide_postgres_metrics_repository, sync_to_thread=False),
    "local_infrastructure_repository": Provide(
        provide_postgres_local_infrastructure_repository,
        sync_to_thread=False,
    ),
    "buffer_service": Provide(provide_shapely_buffer_service, sync_to_thread=False),
    "infrastructure_metrics_service": Provide(
        provide_shapely_infrastructure_metrics_service,
        sync_to_thread=False,
    ),
    "infrastructure_parcel_provider": Provide(
        provide_infrastructure_parcel_provider,
        sync_to_thread=False,
    ),
    "infrastructure_metrics_permission_service": Provide(
        provide_infrastructure_metrics_permission_service,
        sync_to_thread=False,
    ),
    "calculate_infrastructure_metrics_use_case": Provide(
        provide_calculate_infrastructure_metrics_use_case,
        sync_to_thread=False,
    ),
    "get_infrastructure_metrics_use_case": Provide(
        provide_get_infrastructure_metrics_use_case,
        sync_to_thread=False,
    ),
    "get_available_categories_use_case": Provide(
        provide_get_available_categories_use_case,
        sync_to_thread=False,
    ),
    "infrastructure_api": Provide(provide_infrastructure_internal, sync_to_thread=False),
}

__all__ = ("infrastructure_dependencies",)
