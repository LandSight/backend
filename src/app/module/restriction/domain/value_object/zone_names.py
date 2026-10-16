"""Zone names value object."""

from __future__ import annotations

from typing import ClassVar, override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class ZoneNames(BaseValueObject[tuple[str, ...]]):
    """Names of the objects a zone was built from, e.g. a river or a cemetery.

    Names are context for a report, so only a few are kept. Blank names are
    dropped, duplicates merged and the rest sorted.

    Invariants:
    - At most ``MAX_COUNT`` names
    - Each name 1 to ``MAX_NAME_LENGTH`` characters
    """

    MAX_COUNT: ClassVar[int] = 5
    MAX_NAME_LENGTH: ClassVar[int] = 256

    @override
    def _normalize(self, value: tuple[str, ...]) -> tuple[str, ...]:
        names = {" ".join(name.split()) for name in value}
        return tuple(sorted(name for name in names if name))

    @override
    def _validate(self) -> None:
        if len(self._value) > self.MAX_COUNT:
            message = f"At most {self.MAX_COUNT} zone names are kept, got {len(self._value)}."
            raise ValidationError(message)
        too_long = [name for name in self._value if len(name) > self.MAX_NAME_LENGTH]
        if too_long:
            message = f"Zone names must be at most {self.MAX_NAME_LENGTH} characters, got '{too_long[0][:40]}...'."
            raise ValidationError(message)


__all__ = ("ZoneNames",)
