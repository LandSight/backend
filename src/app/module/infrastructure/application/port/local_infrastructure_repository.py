"""Local infrastructure data repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.domain.entity import InfrastructureObject
    from app.module.infrastructure.domain.value_object import Category
    from app.module.shared.interface.internal.geojson import GeoJSONPolygon


class LocalInfrastructureRepository(ABC):
    """Port for reading infrastructure objects from the local data store.

    Implementations:
    - :class:`app.module.infrastructure.infrastructure.repository.postgres_local_infrastructure_repository.PostgresLocalInfrastructureRepository`
    """

    @abstractmethod
    async def get_objects(
        self,
        zone: GeoJSONPolygon,
        category: Category,
    ) -> list[InfrastructureObject]:
        """Return raw infrastructure objects of a category within a zone.

        Parameters
        ----------
        zone : GeoJSONPolygon
            Search zone (buffer ring) to query objects within.
        category : Category
            Infrastructure category to filter objects by.

        Returns
        -------
        list[InfrastructureObject]
            Raw objects of the category located within the zone.
        """
        raise NotImplementedError


__all__ = ("LocalInfrastructureRepository",)
