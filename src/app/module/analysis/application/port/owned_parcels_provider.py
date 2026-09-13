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
    async def list_owned_parcels(self, user_id: UUID) -> dict[UUID, str]:
        """Return the parcels owned by the user as an ``id -> name`` mapping.

        Parameters
        ----------
        user_id : UUID
            ID of the user.

        Returns
        -------
        dict[UUID, str]
            Owned parcel IDs mapped to their names; empty if the user owns none.
        """
        raise NotImplementedError


__all__ = ("OwnedParcelsProvider",)
