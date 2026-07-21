"""Port (abstract base) for the Parcel module's internal API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.parcel.interface.internal.dto import (
        CreateParcelInput,
        DeleteParcelInput,
        GetParcelInput,
        ListUserParcelsInput,
        ParcelListResult,
        ParcelResult,
    )


class ParcelInternalAPI(ABC):
    """Abstract interface for the Parcel module's internal API.

    Implementations:
    - :class:`app.module.parcel.interface.internal.api.ParcelInternal`
    """

    @abstractmethod
    async def create_parcel(self, input_data: CreateParcelInput) -> ParcelResult:
        """Create a new parcel."""
        raise NotImplementedError

    @abstractmethod
    async def get_parcel(self, input_data: GetParcelInput) -> ParcelResult:
        """Get a parcel by ID."""
        raise NotImplementedError

    @abstractmethod
    async def list_user_parcels(self, input_data: ListUserParcelsInput) -> ParcelListResult:
        """List all parcels owned by a user."""
        raise NotImplementedError

    @abstractmethod
    async def delete_parcel(self, input_data: DeleteParcelInput) -> None:
        """Delete a parcel by ID."""
        raise NotImplementedError


__all__ = ("ParcelInternalAPI",)
