"""GeoJSON application DTOs shared across modules.

These are framework-agnostic frozen dataclasses representing the world-
standard GeoJSON geometry format. They are the canonical interchange type used
by the application layer (commands, use cases, services) and referenced by the
internal APIs.

They are **DTOs**, not domain value objects: they carry no business rules --
only structure. Domain value objects (e.g. :class:`~app.module.shared.domain.value_object.Polygon`)
wrap them when invariants are required.

The ``GeoJSONFeature`` and ``GeoJSONFeatureCollection`` types are generic over
their ``properties`` payload so that consumers get full type safety while
remaining serializable (a prerequisite for splitting the modular monolith
into microservices later).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class GeoJSONPoint:
    """GeoJSON Point geometry.

    Examples
    --------
    .. code-block:: python

        GeoJSONPoint(type="Point", coordinates=[37.618423, 55.751244])
    """

    type: str = "Point"
    coordinates: list[float] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class GeoJSONLineString:
    """GeoJSON LineString geometry.

    Examples
    --------
    .. code-block:: python

        GeoJSONLineString(
            type="LineString",
            coordinates=[
                [37.618423, 55.751244],
                [37.628423, 55.761244],
            ],
        )
    """

    type: str = "LineString"
    coordinates: list[list[float]] = field(default_factory=list)


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


# Union of all supported GeoJSON geometries.
GeoJSONGeometry = GeoJSONPoint | GeoJSONLineString | GeoJSONPolygon


@dataclass(frozen=True, slots=True)
class GeoJSONFeature[GeometryT: GeoJSONGeometry, PropertiesT]:
    """GeoJSON Feature.

    A Feature contains a geometry and associated typed properties. The geometry
    type is a parameter, so consumers can pin it (for example a parcel feature
    is always a polygon) while mixed collections use the whole union.
    """

    geometry: GeometryT
    properties: PropertiesT
    type: str = "Feature"


@dataclass(frozen=True, slots=True)
class GeoJSONFeatureCollection[GeometryT: GeoJSONGeometry, PropertiesT]:
    """GeoJSON FeatureCollection.

    A collection of GeoJSON Features sharing the same geometry and properties
    types.
    """

    type: str = "FeatureCollection"
    features: list[GeoJSONFeature[GeometryT, PropertiesT]] = field(default_factory=list)


__all__ = (
    "GeoJSONFeature",
    "GeoJSONFeatureCollection",
    "GeoJSONGeometry",
    "GeoJSONLineString",
    "GeoJSONPoint",
    "GeoJSONPolygon",
)
