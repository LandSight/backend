"""Parcel provider port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.shared.application.dto.geojson import GeoJSONPolygon


class ParcelProvider(ABC):
    """Port for fetching an authorized parcel's geometry.

    Returns the parcel polygon only when the current user is allowed to use
    the parcel. The owning module enforces authorization and raises otherwise,
    so the Infrastructure module never re-implements ownership rules.

    Implementations:
    - :class:`app.module.infrastructure.infrastructure.parcel.parcel_provider.ParcelProviderImpl`
    """

    @abstractmethod
    async def get_parcel_polygon(self, parcel_id: UUID, user_id: UUID) -> GeoJSONPolygon:
        """Return the parcel's polygon geometry for an authorized user.

        Parameters
        ----------
        parcel_id : UUID
            ID of the parcel.
        user_id : UUID
            ID of the user performing the request.

        Returns
        -------
        GeoJSONPolygon
            The parcel polygon geometry.

        Raises
        ------
        app.module.shared.application.error.ForbiddenError
            If the user is not allowed to use the parcel.
        """
        raise NotImplementedError


__all__ = ("ParcelProvider",)
