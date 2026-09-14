"""Metrics permission service implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.infrastructure.application.port import MetricsPermissionService
from app.module.parcel.interface.internal.dto import CheckParcelOwnershipInput


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.parcel.interface.internal.port import ParcelInternalAPI


class MetricsPermissionServiceImpl(MetricsPermissionService):
    """Metrics permission service backed by the Parcel module's Internal API.

    Resolves parcel ownership by delegating to the Parcel module. The
    dependency on :class:`ParcelInternalAPI` is an abstraction wired at the
    composition root, so the Infrastructure application layer stays decoupled
    from the Parcel module.
    """

    def __init__(self, parcel_api: ParcelInternalAPI) -> None:
        self._parcel_api = parcel_api

    @override
    async def user_can_view_parcel_metrics(self, user_id: UUID, parcel_id: UUID) -> bool:
        """See :class:`app.module.infrastructure.application.port.MetricsPermissionService.user_can_view_parcel_metrics`."""
        return await self._parcel_api.is_user_owns_parcel(
            CheckParcelOwnershipInput(user_id=user_id, parcel_id=parcel_id),
        )


__all__ = ("MetricsPermissionServiceImpl",)
