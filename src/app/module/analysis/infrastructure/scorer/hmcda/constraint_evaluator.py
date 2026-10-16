"""Constraint evaluator: applies restriction zones to a multi-criteria score."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from app.module.analysis.domain.value_object import AnalysisScore, AppliedConstraint, ConstraintEffect


if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from app.module.analysis.domain.value_object import RestrictionHit
    from app.module.analysis.infrastructure.scorer.hmcda.config.models import ConstraintRuleConfig


class ConstraintEvaluator:
    """Turns restriction hits into prohibitions and penalties.

    The multi-criteria score says how good a parcel is; constraints say what
    the law or the surroundings rule out. A prohibition zeroes the total score
    whatever the breakdown, penalties multiply it. Hits of kinds without
    a rule have no effect, and so does a penalty scaled by a negligible share.
    """

    # A scaled penalty below this (e.g. a 1 m2 corner in a shore strip) changes
    # nothing a reader could see in a score rounded to two decimals.
    _NEGLIGIBLE_PENALTY = 1e-3

    def __init__(self, rules: Mapping[str, ConstraintRuleConfig]) -> None:
        self._rules = dict(rules)

    def apply(
        self,
        base_score: AnalysisScore,
        hits: Sequence[RestrictionHit],
    ) -> tuple[AnalysisScore, tuple[AppliedConstraint, ...]]:
        """Apply the constraint policy to a base score.

        Parameters
        ----------
        base_score : AnalysisScore
            Score of the multi-criteria breakdown.
        hits : Sequence[RestrictionHit]
            Restrictions on the parcel.

        Returns
        -------
        tuple[AnalysisScore, tuple[AppliedConstraint, ...]]
            The total score and the constraints that changed it, prohibitions
            first, then penalties from the strongest.
        """
        applied = [constraint for hit in hits if (constraint := self._apply_one(hit)) is not None]
        applied.sort(key=lambda constraint: (constraint.effect is not ConstraintEffect.PROHIBIT, constraint.factor))

        factor = math.prod(constraint.factor for constraint in applied)
        return AnalysisScore(base_score.unwrap() * factor), tuple(applied)

    def _apply_one(self, hit: RestrictionHit) -> AppliedConstraint | None:
        """Resolve the effect of one hit, or ``None`` when it has none."""
        rule = self._rules.get(hit.kind)
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


__all__ = ("ConstraintEvaluator",)
