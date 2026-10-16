"""Slope percentiles value object."""

from __future__ import annotations

from typing import ClassVar, override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject
from app.module.topography.domain.value_object.metric import Percentage, Slope


class SlopePercentiles(BaseValueObject[dict[Percentage, Slope]]):
    """Slope percentiles value object.

    Stores slope values at the upper percentiles (75, 90), which describe the
    worst terrain of a parcel; lower percentiles repeat the mean slope.
    Keys are :class:`Percentage` (0-100), values are :class:`Slope` (0-90°).

    Invariants:
    - Must contain exactly the keys P75, P90
    """

    PERCENTILES: ClassVar[tuple[int, ...]] = (75, 90)
    _REQUIRED_PERCENTILES: ClassVar[frozenset[Percentage]] = frozenset(Percentage(p) for p in PERCENTILES)

    @override
    def _normalize(self, value: dict[Percentage, Slope]) -> dict[Percentage, Slope]:
        return value

    @override
    def _validate(self) -> None:
        if set(self._value.keys()) != self._REQUIRED_PERCENTILES:
            message = (
                f"Slope percentiles must contain exactly "
                f"{', '.join(f'P{p}' for p in self.PERCENTILES)}, "
                f"got {{{', '.join(str(int(k.unwrap())) for k in sorted(self._value.keys(), key=lambda p: p.unwrap()))}}}."
            )
            raise ValidationError(message)

    def get(self, percentile: Percentage) -> Slope:
        """Get the slope value at a given percentile.

        Parameters
        ----------
        percentile : Percentage
            Percentile key (e.g., ``Percentage(75)``).

        Returns
        -------
        Slope
            Slope value object.
        """
        return self._value[percentile]

    def to_float_dict(self) -> dict[int, float]:
        """Return the underlying values as a plain float dictionary keyed by int."""
        return {int(k.unwrap()): v.unwrap() for k, v in self._value.items()}


__all__ = ("SlopePercentiles",)
