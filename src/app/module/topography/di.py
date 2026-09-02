"""Dependency injection for Topography module."""

from botocore.client import BaseClient as BotoClient
from litestar.di import NamedDependency, Provide
from rasterio.session import AWSSession
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.topography.application.use_case import (
    CalculateTopographyMetricsUseCase,
    GetLatestParcelTopographyMetricsUseCase,
    GetTopographyMetricsUseCase,
    ListParcelTopographyMetricsUseCase,
)
from app.module.topography.infrastructure.dem import NumpyDemMetricsService
from app.module.topography.infrastructure.geo import ShapelyGeometryMetricsService
from app.module.topography.infrastructure.repository import (
    PostgresMetricsRepository,
    S3LocalDemRepository,
)
from app.module.topography.interface.internal.api import TopographyInternal
from app.platform.config.loaders import load_app_config


# ----- Repositories -----
def provide_postgres_metrics_repository(
    session: NamedDependency[AsyncSession],
) -> PostgresMetricsRepository:
    return PostgresMetricsRepository(session)


def provide_s3_local_dem_repository(
    aws_session: NamedDependency[AWSSession],
    s3_boto_client: NamedDependency[BotoClient],
) -> S3LocalDemRepository:
    """Provide S3-backed local DEM repository."""
    app_config = load_app_config()
    return S3LocalDemRepository(aws_session=aws_session, s3_client=s3_boto_client, s3_config=app_config.s3)


# ----- Services -----
def provide_numpy_dem_metrics_service() -> NumpyDemMetricsService:
    return NumpyDemMetricsService()


def provide_shapely_geometry_metrics_service() -> ShapelyGeometryMetricsService:
    return ShapelyGeometryMetricsService()


# ----- Use Cases -----
def provide_calculate_topography_metrics_use_case(
    local_dem_repository: NamedDependency[S3LocalDemRepository],
    dem_metrics_service: NamedDependency[NumpyDemMetricsService],
    geometry_metrics_service: NamedDependency[ShapelyGeometryMetricsService],
    metrics_repository: NamedDependency[PostgresMetricsRepository],
) -> CalculateTopographyMetricsUseCase:
    return CalculateTopographyMetricsUseCase(
        local_dem_repository=local_dem_repository,
        dem_metrics_service=dem_metrics_service,
        geometry_metrics_service=geometry_metrics_service,
        metrics_repository=metrics_repository,
    )


def provide_get_topography_metrics_use_case(
    metrics_repository: NamedDependency[PostgresMetricsRepository],
) -> GetTopographyMetricsUseCase:
    return GetTopographyMetricsUseCase(metrics_repository)


def provide_get_latest_parcel_topography_metrics_use_case(
    metrics_repository: NamedDependency[PostgresMetricsRepository],
) -> GetLatestParcelTopographyMetricsUseCase:
    return GetLatestParcelTopographyMetricsUseCase(metrics_repository)


def provide_list_parcel_topography_metrics_use_case(
    metrics_repository: NamedDependency[PostgresMetricsRepository],
) -> ListParcelTopographyMetricsUseCase:
    return ListParcelTopographyMetricsUseCase(metrics_repository)


# ----- Internal API -----
def provide_topography_internal(
    calculate_topography_metrics_use_case: NamedDependency[CalculateTopographyMetricsUseCase],
    get_topography_metrics_use_case: NamedDependency[GetTopographyMetricsUseCase],
    get_latest_parcel_topography_metrics_use_case: NamedDependency[GetLatestParcelTopographyMetricsUseCase],
    list_parcel_topography_metrics_use_case: NamedDependency[ListParcelTopographyMetricsUseCase],
) -> TopographyInternal:
    return TopographyInternal(
        calculate_use_case=calculate_topography_metrics_use_case,
        get_use_case=get_topography_metrics_use_case,
        get_latest_parcel_use_case=get_latest_parcel_topography_metrics_use_case,
        list_parcel_use_case=list_parcel_topography_metrics_use_case,
    )


topography_dependencies = {
    "metrics_repository": Provide(provide_postgres_metrics_repository, sync_to_thread=False),
    "local_dem_repository": Provide(provide_s3_local_dem_repository, sync_to_thread=False),
    "dem_metrics_service": Provide(provide_numpy_dem_metrics_service, sync_to_thread=False),
    "geometry_metrics_service": Provide(provide_shapely_geometry_metrics_service, sync_to_thread=False),
    "calculate_topography_metrics_use_case": Provide(
        provide_calculate_topography_metrics_use_case, sync_to_thread=False
    ),
    "get_topography_metrics_use_case": Provide(provide_get_topography_metrics_use_case, sync_to_thread=False),
    "get_latest_parcel_topography_metrics_use_case": Provide(
        provide_get_latest_parcel_topography_metrics_use_case,
        sync_to_thread=False,
    ),
    "list_parcel_topography_metrics_use_case": Provide(
        provide_list_parcel_topography_metrics_use_case,
        sync_to_thread=False,
    ),
    "topography_api": Provide(provide_topography_internal, sync_to_thread=False),
}

__all__ = ("topography_dependencies",)
