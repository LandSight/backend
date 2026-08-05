"""Parcel HTTP endpoints."""

from __future__ import annotations

from uuid import UUID

from litestar import delete, get, post
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.schema.parcel import (
    CreateParcelRequest,
    ParcelFeature,
    ParcelFeatureCollection,
    ParcelFeatureProperties,
)
from app.interface.http.util.guards import require_authorization
from app.module.parcel.interface.internal.dto import (
    CreateParcelInput,
    DeleteParcelInput,
    GetParcelInput,
    ListUserParcelsInput,
)
from app.module.parcel.interface.internal.port import ParcelInternalAPI
from app.module.shared.interface.internal.geojson import GeoJSONPolygon


class ParcelController(Controller):
    """Parcel management endpoints."""

    path = "/"
    tags = ("parcels",)
    guards = [require_authorization]

    @post(
        "/",
        status_code=HTTP_201_CREATED,
        description="Create a new parcel.",
    )
    async def create_parcel(
        self,
        data: CreateParcelRequest,
        parcel_api: ParcelInternalAPI,
        current_user: CurrentUser,
    ) -> ParcelFeature:
        """Create a new parcel."""
        result = await parcel_api.create_parcel(
            CreateParcelInput(
                name=data.name,
                polygon=GeoJSONPolygon(
                    type=data.polygon.type,
                    coordinates=data.polygon.coordinates,
                ),
                owner_id=current_user.id,
            )
        )
        return ParcelFeature(
            geometry=result.geometry,
            properties=ParcelFeatureProperties(
                id=result.properties.id,
                name=result.properties.name,
                owner_id=result.properties.owner_id,
            ),
        )

    @get(
        "/",
        status_code=HTTP_200_OK,
        description="List all parcels owned by the current user.",
    )
    async def list_user_parcels(
        self,
        parcel_api: ParcelInternalAPI,
        current_user: CurrentUser,
    ) -> ParcelFeatureCollection:
        """List all parcels owned by the currently authenticated user."""
        result = await parcel_api.list_user_parcels(ListUserParcelsInput(owner_id=current_user.id))
        features = [
            ParcelFeature(
                geometry=r.geometry,
                properties=ParcelFeatureProperties(
                    id=r.properties.id,
                    name=r.properties.name,
                    owner_id=r.properties.owner_id,
                ),
            )
            for r in result.features
        ]
        return ParcelFeatureCollection(features=features, total=len(features))

    @get(
        "/{parcel_id:uuid}",
        status_code=HTTP_200_OK,
        description="Get a parcel by its ID.",
    )
    async def get_parcel(
        self,
        parcel_id: UUID,
        parcel_api: ParcelInternalAPI,
        current_user: CurrentUser,
    ) -> ParcelFeature:
        """Get a parcel by its ID."""
        result = await parcel_api.get_parcel(
            GetParcelInput(
                parcel_id=parcel_id,
                current_user_id=current_user.id,
            )
        )
        return ParcelFeature(
            geometry=result.geometry,
            properties=ParcelFeatureProperties(
                id=result.properties.id,
                name=result.properties.name,
                owner_id=result.properties.owner_id,
            ),
        )

    @delete(
        "/{parcel_id:uuid}",
        status_code=HTTP_204_NO_CONTENT,
        description="Delete a parcel by its ID (owner only).",
    )
    async def delete_parcel(
        self,
        parcel_id: UUID,
        parcel_api: ParcelInternalAPI,
        current_user: CurrentUser,
    ) -> None:
        """Delete a parcel by its ID."""
        await parcel_api.delete_parcel(
            DeleteParcelInput(
                parcel_id=parcel_id,
                current_user_id=current_user.id,
            )
        )


__all__ = ("ParcelController",)
