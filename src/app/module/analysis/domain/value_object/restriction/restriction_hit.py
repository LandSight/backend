"""Restriction hit value object."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from app.module.shared.domain.value_object import Area, Share


@dataclass(frozen=True, slots=True)
class RestrictionHit(BaseCompositeValueObject):
    """A restriction of one kind on the analysed parcel.

    The analysis view of a hit of the restriction module's check: the profile's
    constraint policy decides whether it bars the scenario or lowers the
    score. A zone covers part of the parcel; a restriction of the whole parcel
    (e.g. a land category) covers all of it.

    Attributes
    ----------
    kind : str
        Restriction kind (e.g. ``power_line_zone``).
    overlap_area : Area
        Area of the parcel under the restriction.
    overlap_share : Share
        Share of the parcel under the restriction.
    zone_names : tuple[str, ...]
        Names of the source objects, when known.
    legal_basis : str
        Short reference to the rule that defines the restriction.
    """

    kind: str
    overlap_area: Area
    overlap_share: Share
    zone_names: tuple[str, ...] = field(default_factory=tuple)
    legal_basis: str = ""

    def _validate(self) -> None:
        if not self.kind:
            message = "A restriction hit must name its kind."
            raise ValidationError(message)


__all__ = ("RestrictionHit",)
