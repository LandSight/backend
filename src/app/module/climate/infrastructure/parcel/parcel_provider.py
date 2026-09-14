"""Parcel provider implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.climate.application.port import ParcelProvider
from app.module.parcel.interface.internal.dto import GetParcelInput
from app.module.shared.application.dto.geojson import GeoJSONPolygon


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.parcel.interface.internal.port import ParcelInternalAPI


class ParcelProviderImpl(ParcelProvider):
    """Parcel geometry provider backed by the Parcel module's Internal API.

    Delegates to ``get_parcel``, which resolves the parcel and enforces
    ownership. The interface-level GeoJSON geometry is translated into the
    application-layer GeoJSON DTO used by Climate.
    """

    def __init__(self, parcel_api: ParcelInternalAPI) -> None:
        self._parcel_api = parcel_api

    @override
    async def get_parcel_polygon(self, parcel_id: UUID, user_id: UUID) -> GeoJSONPolygon:
        """See :class:`app.module.climate.application.port.ParcelProvider.get_parcel_polygon`."""
        result = await self._parcel_api.get_parcel(
            GetParcelInput(parcel_id=parcel_id, current_user_id=user_id),
        )
        return GeoJSONPolygon(type=result.geometry.type, coordinates=result.geometry.coordinates)


__all__ = ("ParcelProviderImpl",)
