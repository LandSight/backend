"""Membership function value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.module.interpretation.domain.value_object.value_position import ValuePosition
from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from collections.abc import Mapping


@dataclass(frozen=True, slots=True)
class Membership(BaseCompositeValueObject):
    """Fuzzy membership function a metric was normalized with.

    The parameter names mirror the functions of the analysis module's fuzzy
    normalizer, so the interpretation can tell where a raw value lies relative
    to the function zones and explain why the metric earned (or lost) points.

    Attributes
    ----------
    function : str
        Function name (``z_shaped``, ``s_shaped`` or ``trapezoidal``).
    params : Mapping[str, float]
        Function parameters keyed by name.
    """

    function: str
    params: Mapping[str, float]

    def _validate(self) -> None:
        if not self.function:
            message = "Membership function name must not be empty."
            raise ValidationError(message)

    def position(self, raw_value: float) -> ValuePosition:
        """Return where ``raw_value`` lies relative to the function zones."""
        match self.function:
            case "z_shaped":
                return self._z_shaped(raw_value)
            case "s_shaped":
                return self._s_shaped(raw_value)
            case "trapezoidal":
                return self._trapezoidal(raw_value)
            case _:
                return ValuePosition.UNKNOWN

    def _z_shaped(self, value: float) -> ValuePosition:
        optimal_max = self.params.get("optimal_max")
        acceptable_max = self.params.get("acceptable_max")
        if optimal_max is None or acceptable_max is None:
            return ValuePosition.UNKNOWN
        if value <= optimal_max:
            return ValuePosition.OPTIMAL
        if value >= acceptable_max:
            return ValuePosition.OUT_HIGH
        return ValuePosition.PARTIAL_HIGH

    def _s_shaped(self, value: float) -> ValuePosition:
        minimum = self.params.get("min")
        maximum = self.params.get("max")
        if minimum is None or maximum is None:
            return ValuePosition.UNKNOWN
        if value <= minimum:
            return ValuePosition.OUT_LOW
        if value >= maximum:
            return ValuePosition.OPTIMAL
        return ValuePosition.PARTIAL_LOW

    def _trapezoidal(self, value: float) -> ValuePosition:
        low = self.params.get("low")
        optimal_min = self.params.get("optimal_min")
        optimal_max = self.params.get("optimal_max")
        high = self.params.get("high")
        if low is None or optimal_min is None or optimal_max is None or high is None:
            return ValuePosition.UNKNOWN
        if value <= low:
            return ValuePosition.OUT_LOW
        if value < optimal_min:
            return ValuePosition.PARTIAL_LOW
        if value <= optimal_max:
            return ValuePosition.OPTIMAL
        if value < high:
            return ValuePosition.PARTIAL_HIGH
        return ValuePosition.OUT_HIGH


__all__ = ("Membership",)
