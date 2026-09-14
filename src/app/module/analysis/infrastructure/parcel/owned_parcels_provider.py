"""Owned parcels provider backed by the Parcel module's Internal API."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import OwnedParcelsProvider
from app.module.parcel.interface.internal.dto import ListUserParcelsInput


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.parcel.interface.internal.port import ParcelInternalAPI


class OwnedParcelsProviderImpl(OwnedParcelsProvider):
    """Resolves owned parcels via the Parcel module's Internal API."""

    def __init__(self, parcel_api: ParcelInternalAPI) -> None:
        self._parcel_api = parcel_api

    @override
    async def list_owned_parcels(self, user_id: UUID) -> dict[UUID, str]:
        """See :class:`app.module.analysis.application.port.OwnedParcelsProvider.list_owned_parcels`."""
        result = await self._parcel_api.list_user_parcels(ListUserParcelsInput(owner_id=user_id))
        return {feature.properties.id: feature.properties.name for feature in result.features}


__all__ = ("OwnedParcelsProviderImpl",)
