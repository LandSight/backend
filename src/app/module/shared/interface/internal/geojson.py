"""GeoJSON DTOs for internal module communication.

These are framework-agnostic frozen dataclasses used as the interchange
format between modules and the HTTP layer.

The ``GeoJSONFeature`` and ``GeoJSONFeatureCollection`` types are generic
over their ``properties`` payload so that consumers get full type safety
while remaining serializable (a prerequisite for splitting the modular
monolith into microservices later).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class GeoJSONPolygon:
    """GeoJSON Polygon geometry.

    Examples
    --------
    .. code-block:: python

        GeoJSONPolygon(
            type="Polygon",
            coordinates=[
                [
                    [37.618423, 55.751244],
                    [37.628423, 55.751244],
                    [37.618423, 55.741244],
                    [37.618423, 55.751244],
                ],
            ],
        )
    """

    type: str = "Polygon"
    coordinates: list[list[list[float]]] = field(default_factory=list)


# Union of all supported GeoJSON geometries (only polygon for now)
GeoJSONGeometry = GeoJSONPolygon


@dataclass(frozen=True, slots=True)
class GeoJSONFeature[T]:
    """GeoJSON Feature.

    A Feature contains a geometry and associated typed properties.
    """

    geometry: GeoJSONGeometry
    properties: T
    type: str = "Feature"


@dataclass(frozen=True, slots=True)
class GeoJSONFeatureCollection[T]:
    """GeoJSON FeatureCollection.

    A collection of GeoJSON Features sharing the same properties type.
    """

    type: str = "FeatureCollection"
    features: list[GeoJSONFeature[T]] = field(default_factory=list)


__all__ = (
    "GeoJSONFeature",
    "GeoJSONFeatureCollection",
    "GeoJSONGeometry",
    "GeoJSONPolygon",
)
