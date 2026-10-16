"""Pydantic models for the constraint policy configuration.

The policy is keyed by analysis type and maps each restriction kind to its
effect on the total score. These models are the typed schema of the packaged
``constraints.yaml``.
"""

from __future__ import annotations

from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.module.analysis.domain.value_object.analysis import (
    AnalysisType,  # noqa: TC001 - needed at runtime for pydantic
)


class ConstraintRuleConfig(BaseModel):
    """Policy for one restriction zone kind.

    Attributes
    ----------
    effect : Literal["prohibit", "penalty"]
        ``prohibit`` bars the scenario once the zone covers at least
        ``min_share`` of the parcel; ``penalty`` always lowers the score.
    min_share : float
        Share of the parcel the zone must cover to prohibit. A smaller overlap
        falls back to ``penalty`` when one is set, otherwise has no effect.
    penalty : float | None
        Fraction the score is lowered by, in ``(0, 1)``; the score is
        multiplied by ``1 - penalty``.
    scale_by_share : bool
        Scale the penalty by the share of the parcel inside the zone, for
        zones that only rule out the covered part of the plot (strips, a
        corner under a power line). Nuisance buffers apply in full.
    """

    model_config = ConfigDict(extra="forbid")

    effect: Literal["prohibit", "penalty"]
    min_share: float = Field(default=0.0, ge=0.0, le=1.0)
    penalty: float | None = Field(default=None, gt=0.0, lt=1.0)
    scale_by_share: bool = False

    @model_validator(mode="after")
    def _check_effect(self) -> Self:
        if self.effect == "penalty" and self.penalty is None:
            message = "A 'penalty' constraint must set 'penalty'."
            raise ValueError(message)
        if self.effect == "penalty" and self.min_share:
            message = "'min_share' only applies to 'prohibit' constraints."
            raise ValueError(message)
        if self.scale_by_share and self.penalty is None:
            message = "'scale_by_share' needs a 'penalty' to scale."
            raise ValueError(message)
        return self


class ConstraintProfileConfig(BaseModel):
    """Constraint policy of one analysis profile, keyed by restriction kind."""

    model_config = ConfigDict(extra="forbid")

    constraints: dict[str, ConstraintRuleConfig] = Field(default_factory=dict)


class ConstraintsConfig(BaseModel):
    """Root of the constraint policy configuration, keyed by analysis type."""

    model_config = ConfigDict(extra="forbid")

    profiles: dict[AnalysisType, ConstraintProfileConfig] = Field(min_length=1)


__all__ = ("ConstraintProfileConfig", "ConstraintRuleConfig", "ConstraintsConfig")
