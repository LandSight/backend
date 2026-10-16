"""Analysis engine value object."""

from __future__ import annotations

from enum import StrEnum


class AnalysisEngine(StrEnum):
    """Scoring engine an analysis is evaluated with.

    An engine selects the algorithm that turns collected metrics into a score
    and decides which extensions the evaluation carries.

    ``BASELINE``
        Fuzzy hierarchical MCDA engine. It is the only engine available today
        and produces the ``hierarchical`` extension; a hybrid rules-and-constraints
        engine is planned and will add the ``rule_based`` and ``constraint_based``
        extensions.
    """

    BASELINE = "baseline"


__all__ = ("AnalysisEngine",)
