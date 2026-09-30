"""Top aspect selector."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object import InterpretationPolicy


if TYPE_CHECKING:
    from collections.abc import Sequence

    from app.module.interpretation.domain.value_object import Aspect


class TopAspectSelector:
    """Selects the aspects that contributed most to the total score.

    Weights exposed for the prompt are contribution shares: because the
    aggregator renormalizes weights over the readings that are available, the
    configured weights do not sum to one, so the share of the contribution is
    the comparable value.
    """

    def __init__(self, policy: InterpretationPolicy | None = None) -> None:
        self._policy = policy or InterpretationPolicy()

    @property
    def limit(self) -> int:
        """Maximum number of aspects returned."""
        return self._policy.aspect_limit

    def top_aspects(self, aspects: Sequence[Aspect]) -> tuple[Aspect, ...]:
        """Return the top aspects ordered by contribution descending."""
        ordered = sorted(aspects, key=lambda aspect: aspect.contribution, reverse=True)
        return tuple(ordered[: self.limit])

    @staticmethod
    def weights_context(aspects: Sequence[Aspect]) -> dict[str, float]:
        """Return the contribution share of every aspect."""
        total = sum(aspect.contribution for aspect in aspects)
        if total <= 0:
            return {aspect.key: 0.0 for aspect in aspects}
        return {aspect.key: round(aspect.contribution / total, 4) for aspect in aspects}


__all__ = ("TopAspectSelector",)
