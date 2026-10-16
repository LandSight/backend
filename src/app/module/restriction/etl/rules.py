"""Zone rules: schema and loader for ``zones.yaml``.

A rule selects OSM objects of one layer by their tags and turns each into a
zone of one kind by buffering it. The width is a constant, a step function of
a derived attribute (voltage, area, river length) or a lookup by tag value.
"""

from __future__ import annotations

from enum import StrEnum
from importlib import resources
from typing import Literal, Self

import yaml
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError as PydanticValidationError,
    field_validator,
    model_validator,
)

from app.module.restriction.domain.value_object import (
    LegalBasis,
    RestrictionKind,
)
from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import SemanticVersion


class OsmLayer(StrEnum):
    """osm2pgsql layer a rule reads from."""

    POINT = "point"
    LINE = "line"
    POLYGON = "polygon"


class DerivedAttribute(StrEnum):
    """Attribute computed from an OSM object that a width can depend on."""

    VOLTAGE_KV = "voltage_kv"
    AREA_HA = "area_ha"
    RIVER_LENGTH_KM = "river_length_km"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class WidthStep(_Strict):
    """One step of a width function: ``width_m`` applies up to ``max`` inclusive.

    The last step has no ``max`` and covers everything above.
    """

    max: float | None = None
    width_m: float = Field(ge=0)


class StepWidth(_Strict):
    """Width as a step function of a derived attribute."""

    by: DerivedAttribute
    steps: tuple[WidthStep, ...] = Field(min_length=1)
    # Voltage when the tag is missing, by the value of the ``power`` tag.
    default_kv: dict[str, float] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _check_steps(self) -> Self:
        bounds = [step.max for step in self.steps[:-1]]
        if any(bound is None for bound in bounds):
            message = "Only the last width step may omit 'max'."
            raise ValueError(message)
        if bounds != sorted(bounds):
            message = "Width steps must be ordered by ascending 'max'."
            raise ValueError(message)
        if self.steps[-1].max is not None:
            message = "The last width step must omit 'max' to cover larger values."
            raise ValueError(message)
        if self.default_kv and self.by is not DerivedAttribute.VOLTAGE_KV:
            message = "'default_kv' only applies to widths by voltage."
            raise ValueError(message)
        return self


class TagWidth(_Strict):
    """Width looked up by the value of one tag."""

    by: Literal["tag"]
    tag: str
    values: dict[str, float] = Field(min_length=1)
    default: float | None = None


class ZoneRule(_Strict):
    """One rule that turns OSM objects into zones of one kind.

    Attributes
    ----------
    id : str
        Unique rule name, for logs.
    kind : RestrictionKind
        Kind of the zones the rule produces.
    layer : OsmLayer
        osm2pgsql layer to read.
    match : tuple[dict[str, list[str]], ...]
        Alternative tag sets, any of which selects the object. Within a set
        every key must match one of its values; ``"*"`` matches any value.
        A single mapping in YAML is one alternative.
    exclude : dict[str, list[str]]
        Tags the object must not have, with the same semantics.
    min_area_ha : float | None
        Polygons smaller than this are skipped.
    extra_sql : str | None
        Additional trusted SQL condition over the ``tags`` hstore column.
    width_m : float | None
        Constant buffer width in meters; 0 keeps the object itself.
    width : StepWidth | TagWidth | None
        Variable buffer width, exclusive with ``width_m``.
    legal_basis : str
        Short reference to the rule that defines the zone.
    """

    id: str = Field(pattern=r"^[a-z0-9_]+$")
    kind: RestrictionKind
    layer: OsmLayer
    match: tuple[dict[str, list[str]], ...] = Field(min_length=1)
    exclude: dict[str, list[str]] = Field(default_factory=dict)
    min_area_ha: float | None = Field(default=None, gt=0)
    extra_sql: str | None = None
    width_m: float | None = Field(default=None, ge=0)
    width: StepWidth | TagWidth | None = None
    legal_basis: str = Field(min_length=1, max_length=LegalBasis.MAX_LENGTH)

    @field_validator("match", mode="before")
    @classmethod
    def _wrap_single_match(cls, value: object) -> object:
        return (value,) if isinstance(value, dict) else value

    @model_validator(mode="after")
    def _check_width(self) -> Self:
        if any(not alternative for alternative in self.match):
            message = f"Rule '{self.id}': a match alternative must name at least one tag."
            raise ValueError(message)
        if (self.width_m is None) == (self.width is None):
            message = f"Rule '{self.id}' must set exactly one of 'width_m' or 'width'."
            raise ValueError(message)
        if self.layer is OsmLayer.POINT and self.width_m == 0:
            message = f"Rule '{self.id}': a point needs a positive width to become a zone."
            raise ValueError(message)
        if self.min_area_ha is not None and self.layer is not OsmLayer.POLYGON:
            message = f"Rule '{self.id}': 'min_area_ha' only applies to polygons."
            raise ValueError(message)
        if isinstance(self.width, StepWidth):
            if self.width.by is DerivedAttribute.AREA_HA and self.layer is not OsmLayer.POLYGON:
                message = f"Rule '{self.id}': a width by area only applies to polygons."
                raise ValueError(message)
            if self.width.by in {DerivedAttribute.VOLTAGE_KV, DerivedAttribute.RIVER_LENGTH_KM} and (
                self.layer is not OsmLayer.LINE
            ):
                message = f"Rule '{self.id}': a width by '{self.width.by}' only applies to lines."
                raise ValueError(message)
        return self


class ZoneRules(_Strict):
    """All zone rules with the version declared in the file.

    Attributes
    ----------
    version : str
        Semantic version of the rules, recorded on every zone and every
        restriction check so a stored analysis can be traced to the widths in
        force when it was scored. Bump MAJOR when a kind is removed or renamed,
        MINOR when a kind or rule is added, PATCH when a width or legal basis
        is corrected.
    rules : tuple[ZoneRule, ...]
        The zone rules.
    """

    version: str
    rules: tuple[ZoneRule, ...] = Field(min_length=1)

    @field_validator("version")
    @classmethod
    def _check_version(cls, value: str) -> str:
        try:
            return SemanticVersion(value).unwrap()
        except ValidationError as exc:
            raise ValueError(str(exc)) from exc

    @model_validator(mode="after")
    def _check_ids(self) -> Self:
        ids = [rule.id for rule in self.rules]
        duplicates = sorted({rule_id for rule_id in ids if ids.count(rule_id) > 1})
        if duplicates:
            message = f"Duplicate zone rule ids: {', '.join(duplicates)}."
            raise ValueError(message)
        return self


def parse_zone_rules(text: str) -> ZoneRules:
    """Parse and validate zone rules from YAML text.

    Raises
    ------
    ValidationError
        If the YAML does not match the rule schema.
    """
    data = yaml.safe_load(text) or {}
    try:
        return ZoneRules.model_validate({"version": str(data.get("version", "")), "rules": data.get("zones", ())})
    except PydanticValidationError as exc:
        message = f"Invalid zone rules: {exc}"
        raise ValidationError(message) from exc


def load_zone_rules() -> ZoneRules:
    """Load the packaged ``zones.yaml`` rules."""
    text = resources.files("app.module.restriction.etl").joinpath("zones.yaml").read_text(encoding="utf-8")
    return parse_zone_rules(text)


__all__ = (
    "DerivedAttribute",
    "OsmLayer",
    "StepWidth",
    "TagWidth",
    "WidthStep",
    "ZoneRule",
    "ZoneRules",
    "load_zone_rules",
    "parse_zone_rules",
)
