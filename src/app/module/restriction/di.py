"""Dependency injection for Restriction module."""

from litestar.di import NamedDependency, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.parcel.interface.internal.port import ParcelInternalAPI
from app.module.restriction.application.use_case import (
    CheckParcelRestrictionsUseCase,
    DeleteRestrictionChecksUseCase,
    GetRestrictionCheckUseCase,
)
from app.module.restriction.infrastructure.parcel import ParcelProviderImpl
from app.module.restriction.infrastructure.permission import RestrictionPermissionServiceImpl
from app.module.restriction.infrastructure.repository import PostgresCheckRepository, PostgresZoneRepository
from app.module.restriction.interface.internal.api import RestrictionInternal


# ----- Repositories -----
def provide_restriction_zone_repository(session: NamedDependency[AsyncSession]) -> PostgresZoneRepository:
    return PostgresZoneRepository(session)


def provide_restriction_check_repository(session: NamedDependency[AsyncSession]) -> PostgresCheckRepository:
    return PostgresCheckRepository(session)


# ----- Parcel integration -----
def provide_restriction_parcel_provider(parcel_api: NamedDependency[ParcelInternalAPI]) -> ParcelProviderImpl:
    return ParcelProviderImpl(parcel_api)


def provide_restriction_permission_service(
    parcel_api: NamedDependency[ParcelInternalAPI],
) -> RestrictionPermissionServiceImpl:
    return RestrictionPermissionServiceImpl(parcel_api)


# ----- Use Cases -----
def provide_check_parcel_restrictions_use_case(
    restriction_zone_repository: NamedDependency[PostgresZoneRepository],
    restriction_check_repository: NamedDependency[PostgresCheckRepository],
    restriction_parcel_provider: NamedDependency[ParcelProviderImpl],
) -> CheckParcelRestrictionsUseCase:
    return CheckParcelRestrictionsUseCase(
        zone_repository=restriction_zone_repository,
        check_repository=restriction_check_repository,
        parcel_provider=restriction_parcel_provider,
    )


def provide_get_restriction_check_use_case(
    restriction_check_repository: NamedDependency[PostgresCheckRepository],
    restriction_permission_service: NamedDependency[RestrictionPermissionServiceImpl],
) -> GetRestrictionCheckUseCase:
    return GetRestrictionCheckUseCase(restriction_check_repository, restriction_permission_service)


def provide_delete_restriction_checks_use_case(
    restriction_check_repository: NamedDependency[PostgresCheckRepository],
    restriction_permission_service: NamedDependency[RestrictionPermissionServiceImpl],
) -> DeleteRestrictionChecksUseCase:
    return DeleteRestrictionChecksUseCase(restriction_check_repository, restriction_permission_service)


# ----- Internal API -----
def provide_restriction_internal(
    check_parcel_restrictions_use_case: NamedDependency[CheckParcelRestrictionsUseCase],
    get_restriction_check_use_case: NamedDependency[GetRestrictionCheckUseCase],
    delete_restriction_checks_use_case: NamedDependency[DeleteRestrictionChecksUseCase],
) -> RestrictionInternal:
    return RestrictionInternal(
        check_restrictions_use_case=check_parcel_restrictions_use_case,
        get_check_use_case=get_restriction_check_use_case,
        delete_checks_use_case=delete_restriction_checks_use_case,
    )


restriction_dependencies = {
    "restriction_zone_repository": Provide(provide_restriction_zone_repository, sync_to_thread=False),
    "restriction_check_repository": Provide(provide_restriction_check_repository, sync_to_thread=False),
    "restriction_parcel_provider": Provide(provide_restriction_parcel_provider, sync_to_thread=False),
    "restriction_permission_service": Provide(provide_restriction_permission_service, sync_to_thread=False),
    "check_parcel_restrictions_use_case": Provide(provide_check_parcel_restrictions_use_case, sync_to_thread=False),
    "get_restriction_check_use_case": Provide(provide_get_restriction_check_use_case, sync_to_thread=False),
    "delete_restriction_checks_use_case": Provide(provide_delete_restriction_checks_use_case, sync_to_thread=False),
    "restriction_api": Provide(provide_restriction_internal, sync_to_thread=False),
}

__all__ = ("restriction_dependencies",)
