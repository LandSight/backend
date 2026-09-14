"""Infrastructure object entity."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.infrastructure.domain.value_object import InfrastructureObjectId
from app.module.shared.domain.entity import BaseEntity


if TYPE_CHECKING:
    from app.module.infrastructure.domain.value_object import Category
    from app.module.shared.domain.value_object import GeoPoint, Polygon


class InfrastructureObject(BaseEntity[InfrastructureObjectId]):
    """A single infrastructure object from the data source.

    Represents a raw object (e.g. a school, hospital, shop, transit stop or
    water body) with its identity, category and metadata. The object has a
    geometry that is either a point (for point-based categories) or a polygon
    (for area-based categories such as water bodies).

    Attributes
    ----------
    id : InfrastructureObjectId
        Identifier of the object in the data source.
    category : Category
        Infrastructure category the object belongs to.
    geometry : GeoPoint | Polygon
        Geometry of the object (point or polygon).
    name : str | None
        Optional human-readable name of the object.
    """

    def __init__(
        self,
        id: InfrastructureObjectId,
        category: Category,
        geometry: GeoPoint | Polygon,
        name: str | None = None,
    ) -> None:
        self._category: Category = category
        self._geometry: GeoPoint | Polygon = geometry
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
    def geometry(self) -> GeoPoint | Polygon:
        """Geometry of the object (point or polygon)."""
        return self._geometry

    @property
    def name(self) -> str | None:
        """Optional human-readable name of the object."""
        return self._name


__all__ = ("InfrastructureObject",)
