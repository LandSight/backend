"""Analysis permission service implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import AnalysisPermissionService
from app.module.parcel.interface.internal.dto import CheckParcelOwnershipInput


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.parcel.interface.internal.port import ParcelInternalAPI


class AnalysisPermissionServiceImpl(AnalysisPermissionService):
    """Analysis permission service backed by the Parcel module's Internal API."""

    def __init__(self, parcel_api: ParcelInternalAPI) -> None:
        self._parcel_api = parcel_api

    @override
    async def user_can_view_parcel(self, user_id: UUID, parcel_id: UUID) -> bool:
        """See :class:`app.module.analysis.application.port.AnalysisPermissionService.user_can_view_parcel`."""
        return await self._parcel_api.is_user_owns_parcel(
            CheckParcelOwnershipInput(user_id=user_id, parcel_id=parcel_id),
        )


__all__ = ("AnalysisPermissionServiceImpl",)
