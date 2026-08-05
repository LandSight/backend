"""Internal DTOs for the Parcel module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.module.shared.interface.internal.geojson import (
    GeoJSONFeature,
    GeoJSONFeatureCollection,
)


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.shared.interface.internal.geojson import GeoJSONPolygon


@dataclass(frozen=True, slots=True)
class CreateParcelInput:
    """Input for creating a new parcel."""

    name: str
    polygon: GeoJSONPolygon
    owner_id: UUID


@dataclass(frozen=True, slots=True)
class GetParcelInput:
    """Input for retrieving a parcel by ID."""

    parcel_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class ListUserParcelsInput:
    """Input for listing parcels owned by a user."""

    owner_id: UUID


@dataclass(frozen=True, slots=True)
class DeleteParcelInput:
    """Input for deleting a parcel."""

    parcel_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class ParcelProperties:
    """Typed properties of a parcel GeoJSON Feature."""

    id: UUID
    name: str
    owner_id: UUID


# Result of a single parcel operation: a GeoJSON Feature with typed properties.
ParcelResult = GeoJSONFeature[ParcelProperties]


# Result of listing parcels: a GeoJSON FeatureCollection with typed properties.
ParcelListResult = GeoJSONFeatureCollection[ParcelProperties]


__all__ = (
    "CreateParcelInput",
    "DeleteParcelInput",
    "GetParcelInput",
    "ListUserParcelsInput",
    "ParcelListResult",
    "ParcelProperties",
    "ParcelResult",
)
