"""Restriction permission service implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.parcel.interface.internal.dto import CheckParcelOwnershipInput
from app.module.restriction.application.port import RestrictionPermissionService


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.parcel.interface.internal.port import ParcelInternalAPI


class RestrictionPermissionServiceImpl(RestrictionPermissionService):
    """Restriction permission service backed by the Parcel module's Internal API.

    Resolves parcel ownership by delegating to the Parcel module, so the
    Restriction application layer stays decoupled from it.
    """

    def __init__(self, parcel_api: ParcelInternalAPI) -> None:
        self._parcel_api = parcel_api

    @override
    async def user_can_view_parcel(self, user_id: UUID, parcel_id: UUID) -> bool:
        """See :class:`app.module.restriction.application.port.RestrictionPermissionService.user_can_view_parcel`."""
        return await self._parcel_api.is_user_owns_parcel(
            CheckParcelOwnershipInput(user_id=user_id, parcel_id=parcel_id),
        )


__all__ = ("RestrictionPermissionServiceImpl",)
