"""Internal DTOs for the Parcel module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


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
class ParcelResult:
    """Result of parcel operations."""

    id: UUID
    name: str
    polygon: dict
    owner_id: UUID


@dataclass(frozen=True, slots=True)
class ParcelListResult:
    """Result of listing parcels."""

    parcels: list[ParcelResult] = field(default_factory=list)


__all__ = (
    "CreateParcelInput",
    "DeleteParcelInput",
    "GetParcelInput",
    "ListUserParcelsInput",
    "ParcelListResult",
    "ParcelResult",
)
