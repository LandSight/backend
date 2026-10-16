"""Restriction constraints extractor."""

from __future__ import annotations

import math
from dataclasses import replace
from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object import InterpretationPolicy


if TYPE_CHECKING:
    from collections.abc import Sequence

    from app.module.interpretation.domain.value_object import ConstraintFinding, EvaluationBreakdown


class ConstraintExtractor:
    """Attributes the lost points to the restriction zones and selects the main ones.

    The constraints multiply the score of the aspects by their factors, so the
    points a single zone took away depend on the order they are applied in. The
    attribution splits the lost points in proportion to ``-ln(factor)``
    instead: the result does not depend on the order and the points of all
    zones add up exactly to the score the constraints took away. A prohibition
    sets the score to zero on its own, so the prohibitions share all the lost
    points equally and the penalties get none.
    """

    def __init__(self, policy: InterpretationPolicy | None = None) -> None:
        self._policy = policy or InterpretationPolicy()

    @property
    def limit(self) -> int:
        """Maximum number of zones returned by :meth:`top_constraints`."""
        return self._policy.constraint_limit

    @staticmethod
    def attribute(
        base_score: float,
        total_score: float,
        findings: Sequence[ConstraintFinding],
    ) -> tuple[ConstraintFinding, ...]:
        """Return the findings with the points each of them took away."""
        loss = max(base_score - total_score, 0.0)
        prohibitions = [finding for finding in findings if finding.prohibits]
        if prohibitions:
            share = loss / len(prohibitions)
            return tuple(replace(finding, points_lost=share if finding.prohibits else 0.0) for finding in findings)
        weights = [-math.log(finding.factor) for finding in findings]
        total_weight = sum(weights)
        if loss == 0.0 or total_weight == 0.0:
            return tuple(replace(finding, points_lost=0.0) for finding in findings)
        return tuple(
            replace(finding, points_lost=loss * weight / total_weight)
            for finding, weight in zip(findings, weights, strict=True)
        )

    def top_constraints(self, breakdown: EvaluationBreakdown) -> tuple[ConstraintFinding, ...]:
        """Return up to the policy limit zones that took away the most points."""
        return self.all_constraints(breakdown)[: self.limit]

    @staticmethod
    def all_constraints(breakdown: EvaluationBreakdown) -> tuple[ConstraintFinding, ...]:
        """Return every zone in the order of the explanation.

        Prohibitions first, then by the points taken away, then by the share of
        the score taken away (the penalties outweighed by a prohibition).
        """
        return tuple(
            sorted(
                breakdown.constraints,
                key=lambda finding: (not finding.prohibits, -finding.points_lost, finding.factor),
            )
        )


__all__ = ("ConstraintExtractor",)
