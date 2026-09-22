"""Internal DTOs for the Infrastructure module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.module.shared.interface.internal.geojson import (
    GeoJSONFeature,
    GeoJSONFeatureCollection,
    GeoJSONLineString,
    GeoJSONPoint,
    GeoJSONPolygon,
)


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class CategoryRequestInput:
    """Requested infrastructure category with its own buffer radius."""

    category: str
    buffer: int


@dataclass(frozen=True, slots=True)
class CalculateMetricsInput:
    """Input for calculating infrastructure metrics."""

    parcel_id: UUID
    current_user_id: UUID
    categories: list[CategoryRequestInput] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class GetMetricsInput:
    """Input for retrieving infrastructure metrics by parcel ID."""

    parcel_id: UUID
    current_user_id: UUID
    categories: list[CategoryRequestInput] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class CategoryMetricRefInput:
    """Reference to a specific infrastructure metrics record within a category."""

    category: str
    metrics_id: UUID


@dataclass(frozen=True, slots=True)
class GetMetricsByIdsInput:
    """Input for retrieving specific infrastructure metrics records by their IDs."""

    parcel_id: UUID
    current_user_id: UUID
    metrics: list[CategoryMetricRefInput] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class CategoryInfoResult:
    """Information about an available infrastructure category."""

    category: str
    label: str


@dataclass(frozen=True, slots=True)
class DeleteMetricsInput:
    """Input for deleting infrastructure metrics snapshots by their references."""

    metrics: list[CategoryMetricRefInput] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class GetObjectsInput:
    """Input for retrieving the objects behind a metrics snapshot."""

    category: str
    metrics_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class InfrastructureObjectPropertiesResult:
    """Typed properties of an infrastructure object GeoJSON Feature."""

    osm_id: str
    name: str | None
    category: str


# Object features can be points, lines or polygons, so the geometry parameter of
# the shared GeoJSONFeature is the whole union.
InfrastructureObjectFeatureResult = GeoJSONFeature[
    GeoJSONPoint | GeoJSONLineString | GeoJSONPolygon,
    InfrastructureObjectPropertiesResult,
]

# The result is a plain GeoJSON FeatureCollection: the caller already knows the
# parcel and the category it requested.
InfrastructureObjectFeatureCollectionResult = GeoJSONFeatureCollection[
    GeoJSONPoint | GeoJSONLineString | GeoJSONPolygon,
    InfrastructureObjectPropertiesResult,
]


__all__ = (
    "CalculateMetricsInput",
    "CategoryInfoResult",
    "CategoryMetricRefInput",
    "CategoryRequestInput",
    "DeleteMetricsInput",
    "GetMetricsByIdsInput",
    "GetMetricsInput",
    "GetObjectsInput",
    "InfrastructureObjectFeatureCollectionResult",
    "InfrastructureObjectFeatureResult",
    "InfrastructureObjectPropertiesResult",
)
