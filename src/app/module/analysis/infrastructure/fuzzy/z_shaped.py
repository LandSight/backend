"""Z-shaped decreasing fuzzy membership function."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar

from app.module.analysis.infrastructure.ports import FuzzyFunction
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    from collections.abc import Mapping


class ZShaped(FuzzyFunction):
    """Decreasing membership with a full and a zero plateau.

    Membership is ``1`` for ``x <= optimal_max``, ``0`` for
    ``x >= acceptable_max`` and decreases linearly in between.
    """

    name: ClassVar[str] = "z_shaped"

    def __init__(self, optimal_max: float, acceptable_max: float, unit: str = "") -> None:
        super().__init__(unit)
        if acceptable_max <= optimal_max:
            message = f"Z-shaped function requires acceptable_max > optimal_max, got {acceptable_max} <= {optimal_max}."
            raise ValidationError(message)
        self._optimal_max = float(optimal_max)
        self._acceptable_max = float(acceptable_max)

    def __call__(self, value: float) -> float:
        """See :meth:`FuzzyFunction.__call__`."""
        if value <= self._optimal_max:
            return 1.0
        if value >= self._acceptable_max:
            return 0.0
        return self.clamp(1.0 - (value - self._optimal_max) / (self._acceptable_max - self._optimal_max))

    def params(self) -> Mapping[str, float]:
        """See :meth:`FuzzyFunction.params`."""
        return MappingProxyType({"optimal_max": self._optimal_max, "acceptable_max": self._acceptable_max})


__all__ = ("ZShaped",)
