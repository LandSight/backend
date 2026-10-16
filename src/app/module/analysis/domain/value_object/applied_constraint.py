"""Applied constraint value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.module.analysis.domain.value_object.constraint_effect import ConstraintEffect
from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from app.module.shared.domain.value_object import Area, Share


@dataclass(frozen=True, slots=True)
class AppliedConstraint(BaseCompositeValueObject):
    """A restriction zone that changed the score of an evaluation.

    Attributes
    ----------
    kind : str
        Restriction zone kind (e.g. ``power_line_zone``).
    effect : ConstraintEffect
        Whether the zone bars the scenario or lowers the score.
    factor : float
        Multiplier applied to the score: ``0`` for a prohibition, in
        ``(0, 1)`` for a penalty.
    overlap_share : Share
        Share of the parcel inside the zone.
    overlap_area : Area
        Area of the parcel inside the zone.
    zone_names : tuple[str, ...]
        Names of the source objects, when known.
    legal_basis : str
        Short reference to the rule that defines the zone.
    """

    kind: str
    effect: ConstraintEffect
    factor: float
    overlap_share: Share
    overlap_area: Area
    zone_names: tuple[str, ...] = ()
    legal_basis: str = ""

    def _validate(self) -> None:
        if not self.kind:
            message = "An applied constraint must name its zone kind."
            raise ValidationError(message)
        if self.effect is ConstraintEffect.PROHIBIT and self.factor != 0.0:
            message = f"Prohibition '{self.kind}' must have factor 0, got {self.factor}."
            raise ValidationError(message)
        if self.effect is ConstraintEffect.PENALTY and not 0.0 < self.factor < 1.0:
            message = f"Penalty '{self.kind}' factor must be within (0, 1), got {self.factor}."
            raise ValidationError(message)


__all__ = ("AppliedConstraint",)
