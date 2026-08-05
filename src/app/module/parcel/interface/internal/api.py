"""Concrete implementation of the Parcel module's internal API.

See :class:`app.module.parcel.interface.internal.port.ParcelInternalAPI`
for the abstract interface.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING, override

from app.module.parcel.application.dto.command import (
    CreateParcelCommand,
    DeleteParcelCommand,
    GetParcelCommand,
    ListUserParcelsCommand,
)
from app.module.parcel.interface.internal.dto import (
    CreateParcelInput,
    DeleteParcelInput,
    GetParcelInput,
    ListUserParcelsInput,
    ParcelListResult,
    ParcelProperties,
    ParcelResult,
)
from app.module.parcel.interface.internal.port import ParcelInternalAPI
from app.module.shared.interface.internal.geojson import GeoJSONFeature, GeoJSONPolygon


if TYPE_CHECKING:
    from app.module.parcel.application.dto.response import ParcelResponse
    from app.module.parcel.application.use_case import (
        CreateParcelUseCase,
        DeleteParcelUseCase,
        GetParcelUseCase,
        ListUserParcelsUseCase,
    )


class ParcelInternal(ParcelInternalAPI):
    """Concrete implementation of the Parcel internal API."""

    def __init__(
        self,
        create_parcel_use_case: CreateParcelUseCase,
        get_parcel_use_case: GetParcelUseCase,
        list_user_parcels_use_case: ListUserParcelsUseCase,
        delete_parcel_use_case: DeleteParcelUseCase,
    ) -> None:
        self._create_parcel = create_parcel_use_case
        self._get_parcel = get_parcel_use_case
        self._list_user_parcels = list_user_parcels_use_case
        self._delete_parcel = delete_parcel_use_case

    @override
    async def create_parcel(self, input_data: CreateParcelInput) -> ParcelResult:
        """See :meth:`ParcelInternalAPI.create_parcel`."""
        result = await self._create_parcel(
            CreateParcelCommand(
                name=input_data.name,
                polygon=asdict(input_data.polygon),
                owner_id=input_data.owner_id,
            )
        )
        return self._to_feature(result)

    @override
    async def get_parcel(self, input_data: GetParcelInput) -> ParcelResult:
        """See :meth:`ParcelInternalAPI.get_parcel`."""
        result = await self._get_parcel(
            GetParcelCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self._to_feature(result)

    @override
    async def list_user_parcels(self, input_data: ListUserParcelsInput) -> ParcelListResult:
        """See :meth:`ParcelInternalAPI.list_user_parcels`."""
        results = await self._list_user_parcels(ListUserParcelsCommand(owner_id=input_data.owner_id))
        return ParcelListResult(features=[self._to_feature(r) for r in results])

    @override
    async def delete_parcel(self, input_data: DeleteParcelInput) -> None:
        """See :meth:`ParcelInternalAPI.delete_parcel`."""
        await self._delete_parcel(
            DeleteParcelCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )

    @staticmethod
    def _to_feature(result: ParcelResponse) -> ParcelResult:
        """Convert an application-layer parcel response into a GeoJSON Feature."""
        return GeoJSONFeature[ParcelProperties](
            geometry=GeoJSONPolygon(
                type=result.polygon["type"],
                coordinates=result.polygon["coordinates"],
            ),
            properties=ParcelProperties(
                id=result.id,
                name=result.name,
                owner_id=result.owner_id,
            ),
        )


__all__ = ("ParcelInternal",)
