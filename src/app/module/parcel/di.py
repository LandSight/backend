"""Dependency injection for Parcel module."""

from litestar.di import NamedDependency, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.parcel.application.use_case import (
    CreateParcelUseCase,
    DeleteParcelUseCase,
    GetParcelUseCase,
    ListUserParcelsUseCase,
)
from app.module.parcel.infrastructure.geo import ShapelyPolygonService
from app.module.parcel.infrastructure.permission import ParcelPermissionServiceImpl
from app.module.parcel.infrastructure.repository import PostgresParcelRepository
from app.module.parcel.interface.internal.api import ParcelInternal


# ----- Repositories -----
def provide_postgres_parcel_repository(
    session: NamedDependency[AsyncSession],
) -> PostgresParcelRepository:
    return PostgresParcelRepository(session)


# ----- Permission -----
def provide_parcel_permission_service(
    parcel_repository: NamedDependency[PostgresParcelRepository],
) -> ParcelPermissionServiceImpl:
    return ParcelPermissionServiceImpl(parcel_repository)


# ----- Services -----
def provide_shapely_polygon_service() -> ShapelyPolygonService:
    return ShapelyPolygonService()


# ----- Use Cases -----
def provide_create_parcel_use_case(
    parcel_repository: NamedDependency[PostgresParcelRepository],
    polygon_service: NamedDependency[ShapelyPolygonService],
) -> CreateParcelUseCase:
    return CreateParcelUseCase(parcel_repository, polygon_service)


def provide_get_parcel_use_case(
    parcel_repository: NamedDependency[PostgresParcelRepository],
    polygon_service: NamedDependency[ShapelyPolygonService],
    parcel_permission_service: NamedDependency[ParcelPermissionServiceImpl],
) -> GetParcelUseCase:
    return GetParcelUseCase(parcel_repository, polygon_service, parcel_permission_service)


def provide_list_user_parcels_use_case(
    parcel_repository: NamedDependency[PostgresParcelRepository],
    polygon_service: NamedDependency[ShapelyPolygonService],
) -> ListUserParcelsUseCase:
    return ListUserParcelsUseCase(parcel_repository, polygon_service)


def provide_delete_parcel_use_case(
    parcel_repository: NamedDependency[PostgresParcelRepository],
    parcel_permission_service: NamedDependency[ParcelPermissionServiceImpl],
) -> DeleteParcelUseCase:
    return DeleteParcelUseCase(parcel_repository, parcel_permission_service)


# ----- Internal API -----
def provide_parcel_internal(
    create_parcel_use_case: NamedDependency[CreateParcelUseCase],
    get_parcel_use_case: NamedDependency[GetParcelUseCase],
    list_user_parcels_use_case: NamedDependency[ListUserParcelsUseCase],
    delete_parcel_use_case: NamedDependency[DeleteParcelUseCase],
    parcel_permission_service: NamedDependency[ParcelPermissionServiceImpl],
) -> ParcelInternal:
    return ParcelInternal(
        create_parcel_use_case=create_parcel_use_case,
        get_parcel_use_case=get_parcel_use_case,
        list_user_parcels_use_case=list_user_parcels_use_case,
        delete_parcel_use_case=delete_parcel_use_case,
        parcel_permission_service=parcel_permission_service,
    )


parcel_dependencies = {
    "parcel_repository": Provide(provide_postgres_parcel_repository, sync_to_thread=False),
    "parcel_permission_service": Provide(provide_parcel_permission_service, sync_to_thread=False),
    "polygon_service": Provide(provide_shapely_polygon_service, sync_to_thread=False),
    "create_parcel_use_case": Provide(provide_create_parcel_use_case, sync_to_thread=False),
    "get_parcel_use_case": Provide(provide_get_parcel_use_case, sync_to_thread=False),
    "list_user_parcels_use_case": Provide(provide_list_user_parcels_use_case, sync_to_thread=False),
    "delete_parcel_use_case": Provide(provide_delete_parcel_use_case, sync_to_thread=False),
    "parcel_api": Provide(provide_parcel_internal, sync_to_thread=False),
}

__all__ = ("parcel_dependencies",)
