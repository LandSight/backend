"""Restriction check response DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import datetime
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class RestrictionHitResponse:
    """Zones of one kind that overlap a parcel.

    Attributes
    ----------
    kind : str
        Zone kind.
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
class RestrictionCheckResponse:
    """Snapshot of the restriction zones that overlap a parcel.

    Attributes
    ----------
    id : UUID
        Snapshot ID.
    parcel_id : UUID
        ID of the checked parcel.
    rules_version : str
        Version of the zone rules the zones were built with.
    created_at : datetime | None
        When the check was made (UTC).
    hits : list[RestrictionHitResponse]
        One entry per overlapping zone kind.
    """

    id: UUID
    parcel_id: UUID
    rules_version: str
    created_at: datetime.datetime | None
    hits: list[RestrictionHitResponse] = field(default_factory=list)


__all__ = ("RestrictionCheckResponse", "RestrictionHitResponse")
