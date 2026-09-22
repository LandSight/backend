"""Infrastructure objects response DTOs."""

from __future__ import annotations

from dataclasses import dataclass

from app.module.shared.application.dto.geojson import (
    GeoJSONFeature,
    GeoJSONFeatureCollection,
    GeoJSONLineString,
    GeoJSONPoint,
    GeoJSONPolygon,
)


@dataclass(frozen=True, slots=True)
class InfrastructureObjectProperties:
    """Typed properties of an infrastructure object GeoJSON Feature.

    Attributes
    ----------
    osm_id : str
        OSM identifier of the object.
    name : str | None
        Human-readable name of the object, if any.
    category : str
        Infrastructure category the object belongs to.
    """

    osm_id: str
    name: str | None
    category: str


# Object features can be points, lines or polygons, so the geometry parameter of
# the shared GeoJSONFeature is the whole union.
InfrastructureObjectFeature = GeoJSONFeature[
    GeoJSONPoint | GeoJSONLineString | GeoJSONPolygon,
    InfrastructureObjectProperties,
]

# The response is a plain GeoJSON FeatureCollection: the caller already knows the
# parcel and the category it requested.
InfrastructureObjectFeatureCollection = GeoJSONFeatureCollection[
    GeoJSONPoint | GeoJSONLineString | GeoJSONPolygon,
    InfrastructureObjectProperties,
]


__all__ = (
    "InfrastructureObjectFeature",
    "InfrastructureObjectFeatureCollection",
    "InfrastructureObjectProperties",
)
