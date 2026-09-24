"""Infrastructure object entity."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.infrastructure.domain.value_object import InfrastructureObjectId
from app.module.shared.domain.entity import BaseEntity


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.infrastructure.domain.value_object import Category
    from app.module.shared.domain.value_object import GeoPoint, LineString, Polygon


class InfrastructureObject(BaseEntity[InfrastructureObjectId]):
    """A single infrastructure object from the data source.

    Represents a raw object (e.g. a school, hospital, grocery shop, transit
    stop or water body) with its identity, category and metadata. The object has
    a geometry that is a point, a polyline (roads, pipelines, power lines,
    rivers) or a polygon (area-based categories such as water bodies and
    forests).

    Attributes
    ----------
    id : InfrastructureObjectId
        Identifier of the object in the data source.
    category : Category
        Infrastructure category the object belongs to.
    geometry : GeoPoint | LineString | Polygon
        Geometry of the object.
    name : str | None
        Optional human-readable name of the object.
    tags : Mapping[str, str] | None
        Raw OSM tags of the object, used to split coarse categories into
        individual metrics (e.g. forest vs. protected area).
    """

    def __init__(
        self,
        id: InfrastructureObjectId,
        category: Category,
        geometry: GeoPoint | LineString | Polygon,
        name: str | None = None,
        tags: Mapping[str, str] | None = None,
    ) -> None:
        self._category: Category = category
        self._geometry: GeoPoint | LineString | Polygon = geometry
        self._name: str | None = name
        self._tags: Mapping[str, str] | None = tags

        super().__init__(id)

    @override
    def _validate(self) -> None:
        pass

    @property
    def category(self) -> Category:
        """Infrastructure category the object belongs to."""
        return self._category

    @property
    def geometry(self) -> GeoPoint | LineString | Polygon:
        """Geometry of the object."""
        return self._geometry

    @property
    def name(self) -> str | None:
        """Optional human-readable name of the object."""
        return self._name

    @property
    def tags(self) -> Mapping[str, str] | None:
        """Raw OSM tags of the object."""
        return self._tags

    def tag(self, key: str) -> str | None:
        """Return a single OSM tag value, or ``None`` when absent."""
        if self._tags is None:
            return None
        return self._tags.get(key)


__all__ = ("InfrastructureObject",)
