"""Infrastructure object entity."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.infrastructure.domain.value_object import InfrastructureObjectId
from app.module.shared.domain.entity import BaseEntity


if TYPE_CHECKING:
    from app.module.infrastructure.domain.value_object import Category
    from app.module.shared.domain.value_object import GeoPoint


class InfrastructureObject(BaseEntity[InfrastructureObjectId]):
    """A single infrastructure object from the data source.

    Represents a raw object (e.g. a school, hospital, shop or transit stop)
    with its identity, category and metadata. The object is located at a
    point (``location``); for the current metrics only the location is used,
    but the metadata is kept for future use (e.g. listing/visualization).

    Attributes
    ----------
    id : InfrastructureObjectId
        Identifier of the object in the data source.
    category : Category
        Infrastructure category the object belongs to.
    name : str | None
        Optional human-readable name of the object.
    location : GeoPoint
        Point location of the object.
    """

    def __init__(
        self,
        id: InfrastructureObjectId,
        category: Category,
        location: GeoPoint,
        name: str | None = None,
    ) -> None:
        self._category: Category = category
        self._location: GeoPoint = location
        self._name: str | None = name

        super().__init__(id)

    @override
    def _validate(self) -> None:
        pass

    @property
    def category(self) -> Category:
        """Infrastructure category the object belongs to."""
        return self._category

    @property
    def location(self) -> GeoPoint:
        """Point location of the object."""
        return self._location

    @property
    def name(self) -> str | None:
        """Optional human-readable name of the object."""
        return self._name


__all__ = ("InfrastructureObject",)
