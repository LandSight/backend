"""Constraint finding value object."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


# English names of the restriction zone kinds, for prompts and reports. An
# unknown kind falls back to its key with spaces.
_KIND_LABELS: Final[dict[str, str]] = {
    "protected_area": "protected natural area",
    "protected_area_buffer": "buffer zone of a protected natural area",
    "power_line_zone": "power line protection zone",
    "gas_distribution_zone": "gas pipeline protection zone",
    "trunk_pipeline_zone": "trunk pipeline protection zone",
    "trunk_pipeline_min_distance": "minimum distance zone of a trunk pipeline",
    "railway_strip": "railway right-of-way",
    "railway_sanitary_gap": "railway sanitary gap",
    "road_body": "road carriageway",
    "roadside_strip": "roadside strip",
    "water_body": "water body",
    "shore_strip": "public shore strip",
    "coastal_protection_strip": "coastal protection strip",
    "water_protection_zone": "water protection zone",
    "wetland": "wetland",
    "cemetery": "cemetery",
    "cemetery_szz": "sanitary protection zone of a cemetery",
    "landfill": "landfill",
    "landfill_szz": "sanitary protection zone of a landfill",
    "wastewater_szz": "sanitary protection zone of a wastewater plant",
    "industrial": "industrial area",
    "industrial_buffer": "buffer around an industrial area",
    "airfield": "airfield",
    "airfield_vicinity": "airfield vicinity",
    "military": "military area",
    "prison": "prison",
    "prison_buffer": "area around a prison",
}

_PROHIBIT: Final = "prohibit"
_PENALTY: Final = "penalty"


@dataclass(frozen=True, slots=True)
class ConstraintFinding(BaseCompositeValueObject):
    """A restriction zone that barred the scenario or lowered the score.

    Attributes
    ----------
    kind : str
        Restriction zone kind (e.g. ``power_line_zone``).
    effect : str
        ``prohibit`` or ``penalty``.
    factor : float
        Multiplier applied to the score.
    overlap_share : float
        Share of the parcel inside the zone, in ``[0, 1]``.
    zone_names : tuple[str, ...]
        Names of the source objects, when known.
    legal_basis : str
        Short reference to the rule that defines the zone.
    points_lost : float
        Points of the total score attributed to the zone (see
        :class:`~app.module.interpretation.domain.service.ConstraintExtractor`);
        the points of all zones add up to the score the constraints took away.
    """

    kind: str
    effect: str
    factor: float
    overlap_share: float
    zone_names: tuple[str, ...] = field(default_factory=tuple)
    legal_basis: str = ""
    points_lost: float = 0.0

    def _validate(self) -> None:
        if self.effect not in {_PROHIBIT, _PENALTY}:
            message = f"Constraint '{self.kind}' effect must be '{_PROHIBIT}' or '{_PENALTY}', got '{self.effect}'."
            raise ValidationError(message)
        if not 0.0 <= self.factor <= 1.0:
            message = f"Constraint '{self.kind}' factor must be within [0, 1], got {self.factor}."
            raise ValidationError(message)
        if not 0.0 <= self.overlap_share <= 1.0:
            message = f"Constraint '{self.kind}' overlap share must be within [0, 1], got {self.overlap_share}."
            raise ValidationError(message)
        if self.points_lost < 0.0:
            message = f"Constraint '{self.kind}' points lost must not be negative, got {self.points_lost}."
            raise ValidationError(message)

    @property
    def prohibits(self) -> bool:
        """Whether the zone bars the scenario on the parcel."""
        return self.effect == _PROHIBIT

    @property
    def label(self) -> str:
        """Human-readable name of the zone kind."""
        return _KIND_LABELS.get(self.kind, self.kind.replace("_", " "))

    @property
    def score_reduction(self) -> float:
        """Share of the score the zone takes away, in ``[0, 1]``."""
        return 1.0 - self.factor


__all__ = ("ConstraintFinding",)
