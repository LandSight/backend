"""Parcels service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


class ParcelsService(ABC):
    """Gateway to the Parcel module's internal API.

    Implementations:
    - :class:`app.module.analysis.infrastructure.gateway.parcels_service.ParcelsServiceImpl`
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


__all__ = ("ParcelsService",)
