"""Parcel endpoints."""

from litestar import delete, get, post
from litestar.controller import Controller
from litestar.di import NamedDependency
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.module.parcel.application.dto.command import (
    CreateParcelCommand,
    DeleteParcelCommand,
    GetParcelCommand,
    ListUserParcelsCommand,
)
from app.module.parcel.application.use_case import (
    CreateParcelUseCase,
    DeleteParcelUseCase,
    GetParcelUseCase,
    ListUserParcelsUseCase,
)
from app.module.parcel.interface.http.schema.parcel import (
    CreateParcelRequest,
    ParcelFeature,
    ParcelFeatureCollection,
    ParcelFeatureProperties,
)
from app.module.shared.application.dto.response import CurrentUser
from app.module.shared.interface.http.guards import require_authorization


class ParcelController(Controller):
    """Parcel management endpoints."""

    path = "/api/v1/parcels"
    tags = ("parcels",)
    guards = [require_authorization]  # noqa: RUF012

    @post(
        "/",
        status_code=HTTP_201_CREATED,
        description="Create a new parcel.",
    )
    async def create_parcel(
        self,
        data: CreateParcelRequest,
        create_parcel_use_case: NamedDependency[CreateParcelUseCase],
        current_user: CurrentUser,
    ) -> ParcelFeature:
        """Create a new parcel.

        Parameters
        ----------
        data : CreateParcelRequest
            Parcel data.
        create_parcel_use_case : CreateParcelUseCase
            Injected use case.
        current_user : CurrentUser
            The currently authenticated user (resolved from token).

        Returns
        -------
        ParcelFeature
            Created parcel as a GeoJSON Feature.
        """
        command = CreateParcelCommand(
            name=data.name,
            polygon=data.polygon.model_dump(),
            owner_id=current_user.id,
        )
        result = await create_parcel_use_case(command)

        return ParcelFeature(
            geometry=result.polygon,
            properties=ParcelFeatureProperties(
                id=result.id,
                name=result.name,
                owner_id=result.owner_id,
            ),
        )

    @get(
        "/",
        status_code=HTTP_200_OK,
        description="List all parcels owned by the current user.",
    )
    async def list_user_parcels(
        self,
        list_user_parcels_use_case: NamedDependency[ListUserParcelsUseCase],
        current_user: CurrentUser,
    ) -> ParcelFeatureCollection:
        """List all parcels owned by the currently authenticated user.

        Parameters
        ----------
        list_user_parcels_use_case : ListUserParcelsUseCase
            Injected use case.
        current_user : CurrentUser
            The currently authenticated user (resolved from token).

        Returns
        -------
        ParcelFeatureCollection
            List of parcels as a GeoJSON FeatureCollection.
        """
        command = ListUserParcelsCommand(owner_id=current_user.id)
        results = await list_user_parcels_use_case(command)

        features = [
            ParcelFeature(
                geometry=r.polygon,
                properties=ParcelFeatureProperties(
                    id=r.id,
                    name=r.name,
                    owner_id=r.owner_id,
                ),
            )
            for r in results
        ]

        return ParcelFeatureCollection(features=features, total=len(features))

    @get(
        "/{parcel_id:str}",
        status_code=HTTP_200_OK,
        description="Get a parcel by its ID.",
    )
    async def get_parcel(
        self,
        parcel_id: str,
        get_parcel_use_case: NamedDependency[GetParcelUseCase],
        current_user: CurrentUser,
    ) -> ParcelFeature:
        """Get a parcel by its ID.

        Parameters
        ----------
        parcel_id : str
            Parcel identifier from the path.
        get_parcel_use_case : GetParcelUseCase
            Injected use case.
        current_user : CurrentUser
            The currently authenticated user (resolved from token).

        Returns
        -------
        ParcelFeature
            Parcel as a GeoJSON Feature.
        """
        command = GetParcelCommand(
            parcel_id=parcel_id,
            current_user_id=current_user.id,
        )
        result = await get_parcel_use_case(command)

        return ParcelFeature(
            geometry=result.polygon,
            properties=ParcelFeatureProperties(
                id=result.id,
                name=result.name,
                owner_id=result.owner_id,
            ),
        )

    @delete(
        "/{parcel_id:str}",
        status_code=HTTP_204_NO_CONTENT,
        description="Delete a parcel by its ID (owner only).",
    )
    async def delete_parcel(
        self,
        parcel_id: str,
        delete_parcel_use_case: NamedDependency[DeleteParcelUseCase],
        current_user: CurrentUser,
    ) -> None:
        """Delete a parcel by its ID.

        Only the owner of the parcel can delete it.

        Parameters
        ----------
        parcel_id : str
            Parcel identifier from the path.
        delete_parcel_use_case : DeleteParcelUseCase
            Injected use case.
        current_user : CurrentUser
            The currently authenticated user (resolved from token).
        """
        command = DeleteParcelCommand(
            parcel_id=parcel_id,
            current_user_id=current_user.id,
        )
        await delete_parcel_use_case(command)


__all__ = ("ParcelController",)
