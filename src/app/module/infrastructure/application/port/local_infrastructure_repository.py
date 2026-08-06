"""Local infrastructure data repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.domain.entity import InfrastructureObject
    from app.module.infrastructure.domain.value_object import BufferZone, Category


class LocalInfrastructureRepository(ABC):
    """Port for reading infrastructure objects from the local data store.

    Implementations:
    - :class:`app.module.infrastructure.infrastructure.repository.postgres_local_infrastructure_repository.PostgresLocalInfrastructureRepository`
    """

    @abstractmethod
    async def get_point_objects(
        self,
        zone: BufferZone,
        category: Category,
    ) -> list[InfrastructureObject]:
        """Return point-based infrastructure objects of a category within a zone.

        Parameters
        ----------
        zone : BufferZone
            Search zone (buffer ring) to query objects within.
        category : Category
            Infrastructure category to filter objects by.

        Returns
        -------
        list[InfrastructureObject]
            Point-based objects of the category located within the zone.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_polygon_objects(
        self,
        zone: BufferZone,
        category: Category,
    ) -> list[InfrastructureObject]:
        """Return polygon-based infrastructure objects of a category within a zone.

        Parameters
        ----------
        zone : BufferZone
            Search zone (buffer ring) to query objects within.
        category : Category
            Infrastructure category to filter objects by.

        Returns
        -------
        list[InfrastructureObject]
            Polygon-based objects of the category located within the zone.
        """
        raise NotImplementedError


__all__ = ("LocalInfrastructureRepository",)
