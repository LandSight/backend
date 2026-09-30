"""S-shaped increasing fuzzy membership function."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar

from app.module.analysis.infrastructure.ports import FuzzyFunction
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    from collections.abc import Mapping


class SShaped(FuzzyFunction):
    """Increasing membership with a zero and a full plateau.

    Membership is ``0`` for ``x <= min``, ``1`` for ``x >= max`` and increases
    linearly in between.
    """

    name: ClassVar[str] = "s_shaped"

    def __init__(self, minimum: float, maximum: float, unit: str = "") -> None:
        super().__init__(unit)
        if maximum <= minimum:
            message = f"S-shaped function requires max > min, got {maximum} <= {minimum}."
            raise ValidationError(message)
        self._minimum = float(minimum)
        self._maximum = float(maximum)

    def __call__(self, value: float) -> float:
        """See :meth:`FuzzyFunction.__call__`."""
        if value <= self._minimum:
            return 0.0
        if value >= self._maximum:
            return 1.0
        return self.clamp((value - self._minimum) / (self._maximum - self._minimum))

    def params(self) -> Mapping[str, float]:
        """See :meth:`FuzzyFunction.params`."""
        return MappingProxyType({"min": self._minimum, "max": self._maximum})


__all__ = ("SShaped",)
