"""Parcel endpoints."""

from typing import Annotated

from litestar import delete, get, post
from litestar.controller import Controller
from litestar.di import NamedDependency
from litestar.params import HeaderParameter
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
    ParcelListResponse,
    ParcelResponse,
)
from app.module.shared.application.port import CurrentUserProvider


class ParcelController(Controller):
    """Parcel management endpoints."""

    path = "/api/v1/parcels"
    tags = ("parcels",)

    @post(
        "/",
        status_code=HTTP_201_CREATED,
        description="Create a new parcel.",
    )
    async def create_parcel(
        self,
        data: CreateParcelRequest,
        create_parcel_use_case: NamedDependency[CreateParcelUseCase],
        current_user_provider: NamedDependency[CurrentUserProvider],
        authorization: Annotated[str, HeaderParameter(name="Authorization", required=True)],
    ) -> ParcelResponse:
        """Create a new parcel.

        Parameters
        ----------
        data : CreateParcelRequest
            Parcel data.
        create_parcel_use_case : CreateParcelUseCase
            Injected use case.
        current_user_provider : CurrentUserProvider
            Injected provider for extracting user ID from the token.
        authorization : str
            Raw Authorization header value.

        Returns
        -------
        ParcelResponse
            Created parcel data.
        """
        token = (authorization or "").removeprefix("Bearer ")
        current_user_id = await current_user_provider.get_current_user_id(token)

        command = CreateParcelCommand(
            name=data.name,
            polygon=data.polygon,
            owner_id=current_user_id,
        )
        result = await create_parcel_use_case(command)

        return ParcelResponse(
            id=result.id,
            name=result.name,
            polygon=result.polygon,
            owner_id=result.owner_id,
        )

    @get(
        "/",
        status_code=HTTP_200_OK,
        description="List all parcels owned by the current user.",
    )
    async def list_user_parcels(
        self,
        list_user_parcels_use_case: NamedDependency[ListUserParcelsUseCase],
        current_user_provider: NamedDependency[CurrentUserProvider],
        authorization: Annotated[str, HeaderParameter(name="Authorization", required=True)],
    ) -> ParcelListResponse:
        """List all parcels owned by the currently authenticated user.

        Parameters
        ----------
        list_user_parcels_use_case : ListUserParcelsUseCase
            Injected use case.
        current_user_provider : CurrentUserProvider
            Injected provider for extracting user ID from the token.
        authorization : str
            Raw Authorization header value.

        Returns
        -------
        ParcelListResponse
            List of parcels owned by the user.
        """
        token = (authorization or "").removeprefix("Bearer ")
        current_user_id = await current_user_provider.get_current_user_id(token)

        command = ListUserParcelsCommand(owner_id=current_user_id)
        results = await list_user_parcels_use_case(command)

        parcels = [
            ParcelResponse(
                id=r.id,
                name=r.name,
                polygon=r.polygon,
                owner_id=r.owner_id,
            )
            for r in results
        ]

        return ParcelListResponse(parcels=parcels, total=len(parcels))

    @get(
        "/{parcel_id:str}",
        status_code=HTTP_200_OK,
        description="Get a parcel by its ID.",
    )
    async def get_parcel(
        self,
        parcel_id: str,
        get_parcel_use_case: NamedDependency[GetParcelUseCase],
    ) -> ParcelResponse:
        """Get a parcel by its ID.

        Parameters
        ----------
        parcel_id : str
            Parcel identifier from the path.
        get_parcel_use_case : GetParcelUseCase
            Injected use case.

        Returns
        -------
        ParcelResponse
            Parcel data.
        """
        command = GetParcelCommand(parcel_id=parcel_id)
        result = await get_parcel_use_case(command)

        return ParcelResponse(
            id=result.id,
            name=result.name,
            polygon=result.polygon,
            owner_id=result.owner_id,
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
        current_user_provider: NamedDependency[CurrentUserProvider],
        authorization: Annotated[str, HeaderParameter(name="Authorization", required=True)],
    ) -> None:
        """Delete a parcel by its ID.

        Only the owner of the parcel can delete it.

        Parameters
        ----------
        parcel_id : str
            Parcel identifier from the path.
        delete_parcel_use_case : DeleteParcelUseCase
            Injected use case.
        current_user_provider : CurrentUserProvider
            Injected provider for extracting user ID from the token.
        authorization : str
            Raw Authorization header value.
        """
        token = (authorization or "").removeprefix("Bearer ")
        current_user_id = await current_user_provider.get_current_user_id(token)

        command = DeleteParcelCommand(
            parcel_id=parcel_id,
            current_user_id=current_user_id,
        )
        await delete_parcel_use_case(command)


__all__ = ("ParcelController",)
