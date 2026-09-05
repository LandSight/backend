"""Parcel permission service implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.parcel.application.port import ParcelPermissionService


if TYPE_CHECKING:
    from app.module.parcel.application.port.parcel_repository import ParcelRepository
    from app.module.parcel.domain.value_object import OwnerId, ParcelId


class ParcelPermissionServiceImpl(ParcelPermissionService):
    """Permission service for parcels backed by the parcel repository.

    For now every action (view, use, manage) is restricted to the parcel owner.
    Future policies can broaden these rules without changing callers.
    """

    def __init__(self, parcel_repository: ParcelRepository) -> None:
        self._parcel_repository = parcel_repository

    @override
    async def is_owner(self, user_id: OwnerId, parcel_id: ParcelId) -> bool:
        """See :class:`app.module.parcel.application.port.ParcelPermissionService.is_owner`."""
        parcel = await self._parcel_repository.get_by_id(parcel_id)
        return parcel is not None and parcel.owner_id == user_id

    @override
    async def user_can_view_parcel(self, user_id: OwnerId, parcel_id: ParcelId) -> bool:
        """See :class:`app.module.parcel.application.port.ParcelPermissionService.user_can_view_parcel`."""
        return await self.is_owner(user_id, parcel_id)

    @override
    async def user_can_manage_parcel(self, user_id: OwnerId, parcel_id: ParcelId) -> bool:
        """See :class:`app.module.parcel.application.port.ParcelPermissionService.user_can_manage_parcel`."""
        return await self.is_owner(user_id, parcel_id)


__all__ = ("ParcelPermissionServiceImpl",)
