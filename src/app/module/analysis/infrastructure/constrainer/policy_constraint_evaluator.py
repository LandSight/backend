"""Constraint evaluator driven by the packaged constraint policy."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import ConstraintEvaluator
from app.module.analysis.domain.value_object.constraint import AppliedConstraint, ConstraintEffect
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    from collections.abc import Sequence

    from app.module.analysis.domain.value_object.analysis import AnalysisType
    from app.module.analysis.domain.value_object.restriction import RestrictionHit
    from app.module.analysis.infrastructure.constrainer.config.models import ConstraintRuleConfig, ConstraintsConfig


class PolicyConstraintEvaluator(ConstraintEvaluator):
    """Turns restriction hits into prohibitions and penalties by profile policy.

    A prohibition bars the scenario whatever the breakdown, a penalty lowers
    the score. Hits of kinds without a rule have no effect, and so does a
    penalty scaled by a negligible share. Each kind is judged on its own, so
    kinds overlapping the same part of the plot compound: a deliberately
    conservative overstatement (see ``config/constraints.yaml``).
    """

    # A scaled penalty below this (e.g. a 1 m2 corner in a shore strip) changes
    # nothing a reader could see in a score rounded to two decimals.
    _NEGLIGIBLE_PENALTY = 1e-3

    def __init__(self, config: ConstraintsConfig) -> None:
        self._rules: dict[AnalysisType, dict[str, ConstraintRuleConfig]] = {
            analysis_type: dict(profile.constraints) for analysis_type, profile in config.profiles.items()
        }

    @override
    def evaluate(self, analysis_type: AnalysisType, hits: Sequence[RestrictionHit]) -> tuple[AppliedConstraint, ...]:
        """See :class:`app.module.analysis.application.port.ConstraintEvaluator.evaluate`."""
        rules = self._rules.get(analysis_type)
        if rules is None:
            message = f"No constraint policy configured for analysis type '{analysis_type}'."
            raise ValidationError(message)

        applied = [constraint for hit in hits if (constraint := self._apply_one(rules, hit)) is not None]
        applied.sort(key=lambda constraint: (constraint.effect is not ConstraintEffect.PROHIBIT, constraint.factor))
        return tuple(applied)

    def _apply_one(self, rules: dict[str, ConstraintRuleConfig], hit: RestrictionHit) -> AppliedConstraint | None:
        """Resolve the effect of one hit, or ``None`` when it has none."""
        rule = rules.get(hit.kind)
        if rule is None:
            return None

        share = hit.overlap_share.unwrap()
        if rule.effect == "prohibit" and share >= rule.min_share:
            effect, factor = ConstraintEffect.PROHIBIT, 0.0
        elif rule.penalty is not None:
            weight = share if rule.scale_by_share else 1.0
            effect, factor = ConstraintEffect.PENALTY, 1.0 - rule.penalty * weight
        else:
            return None
        if effect is ConstraintEffect.PENALTY and factor >= 1.0 - self._NEGLIGIBLE_PENALTY:
            return None

        return AppliedConstraint(
            kind=hit.kind,
            effect=effect,
            factor=factor,
            overlap_share=hit.overlap_share,
            overlap_area=hit.overlap_area,
            zone_names=hit.zone_names,
            legal_basis=hit.legal_basis,
        )


__all__ = ("PolicyConstraintEvaluator",)
