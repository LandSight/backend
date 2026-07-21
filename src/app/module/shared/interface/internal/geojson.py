"""GeoJSON DTOs for internal module communication.

These are framework-agnostic frozen dataclasses used as the interchange
format between modules and the HTTP layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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


@dataclass(frozen=True, slots=True)
class GeoJSONFeature:
    """GeoJSON Feature.

    A Feature contains a geometry and associated properties.
    """

    type: str = "Feature"
    geometry: GeoJSONPolygon | None = None
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class GeoJSONFeatureCollection:
    """GeoJSON FeatureCollection.

    A collection of GeoJSON Features.
    """

    type: str = "FeatureCollection"
    features: list[GeoJSONFeature] = field(default_factory=list)


__all__ = (
    "GeoJSONFeature",
    "GeoJSONFeatureCollection",
    "GeoJSONPolygon",
)
