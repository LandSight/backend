"""Dependency injection for Climate module."""

from botocore.client import BaseClient as BotoClient
from litestar.di import NamedDependency, Provide
from rasterio.session import AWSSession
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.climate.application.use_case import (
    CalculateClimateMetricsUseCase,
    GetClimateMetricsUseCase,
    GetParcelClimateMetricsUseCase,
)
from app.module.climate.infrastructure.climate import NumpyClimateMetricsService
from app.module.climate.infrastructure.parcel import ParcelProviderImpl
from app.module.climate.infrastructure.permission import MetricsPermissionServiceImpl
from app.module.climate.infrastructure.repository import (
    PostgresMetricsRepository,
    S3LocalClimateRepository,
)
from app.module.climate.interface.internal.api import ClimateInternal
from app.module.parcel.interface.internal.port import ParcelInternalAPI
from app.platform.config.loaders import load_app_config


# ----- Repositories -----
def provide_postgres_metrics_repository(
    session: NamedDependency[AsyncSession],
) -> PostgresMetricsRepository:
    return PostgresMetricsRepository(session)


def provide_s3_local_climate_repository(
    aws_session: NamedDependency[AWSSession],
    s3_boto_client: NamedDependency[BotoClient],
) -> S3LocalClimateRepository:
    """Provide S3-backed local climate repository."""
    app_config = load_app_config()
    return S3LocalClimateRepository(aws_session=aws_session, s3_client=s3_boto_client, s3_config=app_config.s3)


# ----- Services -----
def provide_numpy_climate_metrics_service() -> NumpyClimateMetricsService:
    return NumpyClimateMetricsService()


# ----- Parcel integration -----
def provide_climate_parcel_provider(
    parcel_api: NamedDependency[ParcelInternalAPI],
) -> ParcelProviderImpl:
    return ParcelProviderImpl(parcel_api)


# ----- Services -----
def provide_climate_metrics_permission_service(
    parcel_api: NamedDependency[ParcelInternalAPI],
) -> MetricsPermissionServiceImpl:
    return MetricsPermissionServiceImpl(parcel_api)


# ----- Use Cases -----
def provide_calculate_climate_metrics_use_case(
    local_climate_repository: NamedDependency[S3LocalClimateRepository],
    climate_metrics_service: NamedDependency[NumpyClimateMetricsService],
    climate_metrics_repository: NamedDependency[PostgresMetricsRepository],
    climate_parcel_provider: NamedDependency[ParcelProviderImpl],
) -> CalculateClimateMetricsUseCase:
    return CalculateClimateMetricsUseCase(
        local_climate_repository=local_climate_repository,
        climate_metrics_service=climate_metrics_service,
        metrics_repository=climate_metrics_repository,
        parcel_provider=climate_parcel_provider,
    )


def provide_get_climate_metrics_use_case(
    climate_metrics_repository: NamedDependency[PostgresMetricsRepository],
    climate_metrics_permission_service: NamedDependency[MetricsPermissionServiceImpl],
) -> GetClimateMetricsUseCase:
    return GetClimateMetricsUseCase(climate_metrics_repository, climate_metrics_permission_service)


def provide_get_parcel_climate_metrics_use_case(
    climate_metrics_repository: NamedDependency[PostgresMetricsRepository],
    climate_metrics_permission_service: NamedDependency[MetricsPermissionServiceImpl],
) -> GetParcelClimateMetricsUseCase:
    return GetParcelClimateMetricsUseCase(climate_metrics_repository, climate_metrics_permission_service)


# ----- Internal API -----
def provide_climate_internal(
    calculate_climate_metrics_use_case: NamedDependency[CalculateClimateMetricsUseCase],
    get_climate_metrics_use_case: NamedDependency[GetClimateMetricsUseCase],
    get_parcel_climate_metrics_use_case: NamedDependency[GetParcelClimateMetricsUseCase],
) -> ClimateInternal:
    return ClimateInternal(
        calculate_metrics_use_case=calculate_climate_metrics_use_case,
        get_metrics_use_case=get_climate_metrics_use_case,
        get_parcel_metrics_use_case=get_parcel_climate_metrics_use_case,
    )


climate_dependencies = {
    "climate_metrics_repository": Provide(provide_postgres_metrics_repository, sync_to_thread=False),
    "climate_metrics_permission_service": Provide(provide_climate_metrics_permission_service, sync_to_thread=False),
    "climate_parcel_provider": Provide(provide_climate_parcel_provider, sync_to_thread=False),
    "local_climate_repository": Provide(provide_s3_local_climate_repository, sync_to_thread=False),
    "climate_metrics_service": Provide(provide_numpy_climate_metrics_service, sync_to_thread=False),
    "calculate_climate_metrics_use_case": Provide(provide_calculate_climate_metrics_use_case, sync_to_thread=False),
    "get_climate_metrics_use_case": Provide(provide_get_climate_metrics_use_case, sync_to_thread=False),
    "get_parcel_climate_metrics_use_case": Provide(
        provide_get_parcel_climate_metrics_use_case,
        sync_to_thread=False,
    ),
    "climate_api": Provide(provide_climate_internal, sync_to_thread=False),
}

__all__ = ("climate_dependencies",)
