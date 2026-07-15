"""GeoJSON schemas for HTTP request/response validation."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class GeoJSONPolygon(BaseModel):
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

    type: str = Field(
        default="Polygon",
        description='GeoJSON geometry type. Must be ``"Polygon"``.',
    )
    coordinates: list[list[list[float]]] = Field(
        description="Polygon coordinates: an array of rings, where each ring is an array of ``[longitude, latitude]`` pairs.",
        min_length=1,
    )


class GeoJSONFeature(BaseModel):
    """GeoJSON Feature.

    A Feature contains a geometry and associated properties.
    """

    type: str = Field(
        default="Feature",
        description='GeoJSON type. Must be ``"Feature"``.',
    )
    geometry: GeoJSONPolygon = Field(
        description="Feature geometry.",
    )
    properties: dict[str, Any] = Field(
        default_factory=dict,
        description="Feature properties.",
    )


class GeoJSONFeatureCollection(BaseModel):
    """GeoJSON FeatureCollection.

    A collection of GeoJSON Features.
    """

    type: str = Field(
        default="FeatureCollection",
        description='GeoJSON type. Must be ``"FeatureCollection"``.',
    )
    features: list[GeoJSONFeature] = Field(
        description="List of GeoJSON Features.",
    )


__all__ = (
    "GeoJSONFeature",
    "GeoJSONFeatureCollection",
    "GeoJSONPolygon",
)
