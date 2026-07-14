"""Parcel repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.parcel.domain.entity.parcel import Parcel
    from app.module.parcel.domain.value_object import OwnerId, ParcelId


class ParcelRepository(ABC):
    """Port for parcel persistence.

    Implementations:
    - :class:`app.module.parcel.infrastructure.repository.postgres_parcel_repository.PostgresParcelRepository`
    """

    @abstractmethod
    async def save(self, parcel: Parcel) -> None:
        """Persist a parcel.

        Parameters
        ----------
        parcel : Parcel
            Parcel entity to save.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, parcel_id: ParcelId) -> Parcel | None:
        """Retrieve a parcel by its ID.

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.

        Returns
        -------
        Parcel | None
            The parcel if found, ``None`` otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_owner_id(self, owner_id: OwnerId) -> list[Parcel]:
        """Retrieve all parcels owned by a specific user.

        Parameters
        ----------
        owner_id : OwnerId
            Owner identifier.

        Returns
        -------
        list[Parcel]
            List of parcels owned by the user.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, parcel_id: ParcelId) -> None:
        """Delete a parcel by its ID.

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.
        """
        raise NotImplementedError


__all__ = ("ParcelRepository",)
