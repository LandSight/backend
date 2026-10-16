"""Restriction check value object."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from app.module.analysis.domain.value_object.restriction_check_ref import RestrictionCheckRef
    from app.module.analysis.domain.value_object.restriction_hit import RestrictionHit


@dataclass(frozen=True, slots=True)
class RestrictionCheck(BaseCompositeValueObject):
    """The restrictions on the analysed parcel, as read from their snapshot.

    Attributes
    ----------
    ref : RestrictionCheckRef
        Reference to the snapshot in the restriction module.
    hits : tuple[RestrictionHit, ...]
        One hit per restriction kind; empty when the parcel is clear.
    """

    ref: RestrictionCheckRef
    hits: tuple[RestrictionHit, ...] = field(default_factory=tuple)

    def _validate(self) -> None:
        kinds = [hit.kind for hit in self.hits]
        if len(kinds) != len(set(kinds)):
            message = "A restriction check must hold at most one hit per kind."
            raise ValidationError(message)


__all__ = ("RestrictionCheck",)
