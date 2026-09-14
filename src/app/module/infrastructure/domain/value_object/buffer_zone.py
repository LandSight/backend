"""Buffer zone value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject, Polygon


class BufferZone(BaseValueObject[tuple[Polygon, Polygon]]):
    """Buffer zone around a parcel represented as a ring.

    The ring is defined by two polygons: the outer boundary of the buffer and
    the inner boundary (the parcel to exclude). Objects of interest lie in the
    area between the two polygons.

    Invariants:
    - Must contain exactly two polygons (outer and inner)
    """

    _EXPECTED_POLYGONS = 2

    @override
    def _normalize(self, value: tuple[Polygon, Polygon]) -> tuple[Polygon, Polygon]:
        return value

    @override
    def _validate(self) -> None:
        if len(self._value) != self._EXPECTED_POLYGONS:
            message = (
                f"BufferZone must contain exactly {self._EXPECTED_POLYGONS} polygons "
                f"(outer and inner), got {len(self._value)}."
            )
            raise ValidationError(message)

    @property
    def outer(self) -> Polygon:
        """Outer boundary of the buffer zone."""
        return self._value[0]

    @property
    def inner(self) -> Polygon:
        """Inner boundary (the parcel) to exclude from the search area."""
        return self._value[1]


__all__ = ("BufferZone",)
