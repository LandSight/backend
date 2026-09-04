"""Parcel provider implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.parcel.interface.internal.dto import GetParcelInput
from app.module.topography.application.port import ParcelProvider


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.parcel.interface.internal.port import ParcelInternalAPI
    from app.module.shared.interface.internal.geojson import GeoJSONPolygon


class ParcelProviderImpl(ParcelProvider):
    """Parcel geometry provider backed by the Parcel module's Internal API.

    Delegates to ``get_parcel``, which resolves the parcel and enforces
    ownership. This way the Parcel module remains the single source of truth
    for both the geometry and the access rule.
    """

    def __init__(self, parcel_api: ParcelInternalAPI) -> None:
        self._parcel_api = parcel_api

    @override
    async def get_parcel_polygon(self, parcel_id: UUID, user_id: UUID) -> GeoJSONPolygon:
        """See :class:`app.module.topography.application.port.ParcelProvider.get_parcel_polygon`."""
        result = await self._parcel_api.get_parcel(
            GetParcelInput(parcel_id=parcel_id, current_user_id=user_id),
        )
        return result.geometry


__all__ = ("ParcelProviderImpl",)
