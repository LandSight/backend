"""Internal DTOs for the Restriction module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import datetime
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class CalculateCheckInput:
    """Input for calculating the restriction check of a parcel."""

    parcel_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class GetCheckInput:
    """Input for retrieving a restriction check snapshot by its ID."""

    check_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class DeleteChecksInput:
    """Input for deleting restriction check snapshots by their IDs.

    The checks must belong to parcels of the current user.
    """

    check_ids: list[UUID]
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class RestrictionHitResult:
    """Zones of one kind that overlap a parcel.

    Attributes
    ----------
    kind : str
        Zone kind (e.g. ``power_line_zone``).
    overlap_area_m2 : float
        Area of the parcel inside the zones, in square meters.
    overlap_share : float
        Share of the parcel area inside the zones, in ``[0, 1]``.
    zone_names : list[str]
        Names of the source objects, when known.
    legal_basis : str
        Short reference to the rule that defines the zone.
    """

    kind: str
    overlap_area_m2: float
    overlap_share: float
    zone_names: list[str] = field(default_factory=list)
    legal_basis: str = ""


@dataclass(frozen=True, slots=True)
class RestrictionCheckResult:
    """Snapshot of the restriction zones that overlap a parcel."""

    id: UUID
    parcel_id: UUID
    rules_version: str
    created_at: datetime.datetime | None
    hits: list[RestrictionHitResult] = field(default_factory=list)


__all__ = (
    "CalculateCheckInput",
    "DeleteChecksInput",
    "GetCheckInput",
    "RestrictionCheckResult",
    "RestrictionHitResult",
)
