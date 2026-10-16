"""Constraint evaluator port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Sequence

    from app.module.analysis.domain.value_object.analysis import AnalysisType
    from app.module.analysis.domain.value_object.constraint import AppliedConstraint
    from app.module.analysis.domain.value_object.restriction import RestrictionHit


class ConstraintEvaluator(ABC):
    """Port for deciding which restrictions constrain an analysis.

    Runs after the scorer and independently of it: the scorer rates a parcel
    from its metrics, the evaluator decides which restrictions bar the
    scenario or lower that score. Applying them to the score is up to
    :meth:`app.module.analysis.domain.entity.AnalysisEvaluation.apply_constraints`.

    Implementations:
    - :class:`app.module.analysis.infrastructure.constrainer.policy_constraint_evaluator.PolicyConstraintEvaluator`
    """

    @abstractmethod
    def evaluate(self, analysis_type: AnalysisType, hits: Sequence[RestrictionHit]) -> tuple[AppliedConstraint, ...]:
        """Return the constraints the restrictions impose on the scenario.

        Parameters
        ----------
        analysis_type : AnalysisType
            Scenario whose policy decides the effect of each restriction.
        hits : Sequence[RestrictionHit]
            Restrictions on the parcel.

        Returns
        -------
        tuple[AppliedConstraint, ...]
            Prohibitions first, then penalties from the strongest; restrictions
            without an effect are left out.
        """
        raise NotImplementedError


__all__ = ("ConstraintEvaluator",)
