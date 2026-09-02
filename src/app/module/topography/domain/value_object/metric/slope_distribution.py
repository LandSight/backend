"""Slope distribution value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject
from app.module.topography.domain.value_object.metric import Percentage


class SlopeDistribution(BaseValueObject[list[Percentage]]):
    """Slope distribution histogram value object.

    Stores a histogram of slope values across the parcel area.
    Contains 10 bins representing equal-width intervals from 0° to 90°.

    Invariants:
    - Must contain exactly 10 bins
    - Values must sum to approximately 100 (±1 for rounding)
    """

    _NUM_BINS = 10
    _TOLERANCE = 1.0

    @override
    def _normalize(self, value: list[Percentage]) -> list[Percentage]:
        return value

    @override
    def _validate(self) -> None:
        if len(self._value) != self._NUM_BINS:
            message = f"Slope distribution must contain exactly {self._NUM_BINS} bins, got {len(self._value)}."
            raise ValidationError(message)

        total = sum(p.unwrap() for p in self._value)
        if abs(total - 100) > self._TOLERANCE:
            message = f"Slope distribution bins must sum to approximately 100, got {total}."
            raise ValidationError(message)

    @property
    def bins(self) -> list[Percentage]:
        """Histogram bins."""
        return list(self._value)

    def to_float_list(self) -> list[float]:
        """Underlying values as a plain float list."""
        return [p.unwrap() for p in self._value]

    @property
    def bin_edges(self) -> list[float]:
        """Edges of each bin in degrees.

        Returns 11 edges for 10 bins: [0, 9, 18, 27, 36, 45, 54, 63, 72, 81, 90].
        """
        step = 90.0 / self._NUM_BINS
        return [round(i * step, 1) for i in range(self._NUM_BINS + 1)]


__all__ = ("SlopeDistribution",)
