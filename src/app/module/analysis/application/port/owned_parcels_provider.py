"""Owned parcels provider port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


class OwnedParcelsProvider(ABC):
    """Port for resolving the parcels owned by a user.

    Implementations:
    - :class:`app.module.analysis.infrastructure.parcel.owned_parcels_provider.OwnedParcelsProviderImpl`
    """

    @abstractmethod
    async def list_owned_parcel_ids(self, user_id: UUID) -> list[UUID]:
        """Return IDs of all parcels owned by the user.

        Parameters
        ----------
        user_id : UUID
            ID of the user.

        Returns
        -------
        list[UUID]
            Owned parcel IDs; empty if the user owns no parcels.
        """
        raise NotImplementedError


__all__ = ("OwnedParcelsProvider",)
