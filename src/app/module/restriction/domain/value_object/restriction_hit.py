"""Restriction hit value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from app.module.restriction.domain.value_object.legal_basis import LegalBasis
    from app.module.restriction.domain.value_object.restriction_kind import RestrictionKind
    from app.module.restriction.domain.value_object.zone_names import ZoneNames
    from app.module.shared.domain.value_object import Area, Share


@dataclass(frozen=True, slots=True)
class RestrictionHit(BaseCompositeValueObject):
    """Zones of one kind that overlap a parcel.

    Overlapping zones of the same kind are merged, so the overlap is counted
    once. Each field validates itself; the hit adds no cross-field rules.

    Attributes
    ----------
    kind : RestrictionKind
        Kind of the zones.
    overlap_area : Area
        Area of the parcel inside the zones.
    overlap_share : Share
        Share of the parcel area inside the zones.
    zone_names : ZoneNames
        Names of the source objects, when known.
    legal_basis : LegalBasis
        Reference to the rule that defines the zone.
    """

    kind: RestrictionKind
    overlap_area: Area
    overlap_share: Share
    zone_names: ZoneNames
    legal_basis: LegalBasis

    def _validate(self) -> None:
        return None


__all__ = ("RestrictionHit",)
