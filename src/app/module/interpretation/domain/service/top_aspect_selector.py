"""Top aspect selector."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object import InterpretationPolicy


if TYPE_CHECKING:
    from collections.abc import Sequence

    from app.module.interpretation.domain.value_object import Aspect


class TopAspectSelector:
    """Selects the aspects that contributed most points to the total score."""

    def __init__(self, policy: InterpretationPolicy | None = None) -> None:
        self._policy = policy or InterpretationPolicy()

    @property
    def limit(self) -> int:
        """Maximum number of aspects returned."""
        return self._policy.aspect_limit

    def top_aspects(self, aspects: Sequence[Aspect]) -> tuple[Aspect, ...]:
        """Return the top aspects ordered by points descending."""
        ordered = sorted(aspects, key=lambda aspect: aspect.points, reverse=True)
        return tuple(ordered[: self.limit])


__all__ = ("TopAspectSelector",)
