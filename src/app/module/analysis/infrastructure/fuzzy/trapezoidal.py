"""Trapezoidal fuzzy membership function."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar

from app.module.analysis.infrastructure.ports import FuzzyFunction
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    from collections.abc import Mapping


class Trapezoidal(FuzzyFunction):
    """Membership with a rising edge, an optimal plateau and a falling edge."""

    name: ClassVar[str] = "trapezoidal"

    def __init__(
        self,
        low: float,
        optimal_min: float,
        optimal_max: float,
        high: float,
        unit: str = "",
    ) -> None:
        super().__init__(unit)
        if not (low < optimal_min <= optimal_max < high):
            message = (
                "Trapezoidal function requires low < optimal_min <= optimal_max < high, "
                f"got low={low}, optimal_min={optimal_min}, optimal_max={optimal_max}, high={high}."
            )
            raise ValidationError(message)
        self._low = float(low)
        self._optimal_min = float(optimal_min)
        self._optimal_max = float(optimal_max)
        self._high = float(high)

    def __call__(self, value: float) -> float:
        """See :meth:`FuzzyFunction.__call__`."""
        if value <= self._low or value >= self._high:
            return 0.0
        if value < self._optimal_min:
            return self.clamp((value - self._low) / (self._optimal_min - self._low))
        if value <= self._optimal_max:
            return 1.0
        return self.clamp(1.0 - (value - self._optimal_max) / (self._high - self._optimal_max))

    def params(self) -> Mapping[str, float]:
        """See :meth:`FuzzyFunction.params`."""
        return MappingProxyType(
            {
                "low": self._low,
                "optimal_min": self._optimal_min,
                "optimal_max": self._optimal_max,
                "high": self._high,
            }
        )


__all__ = ("Trapezoidal",)
