"""Grade verdict value object."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


@dataclass(frozen=True, slots=True)
class GradeVerdict(BaseCompositeValueObject):
    """Outcome of verifying a generated explanation against its source facts.

    Attributes
    ----------
    ok : bool
        Whether the explanation passed verification.
    issues : tuple[str, ...]
        Human-readable reasons the explanation was rejected.
    corrected_text : str | None
        Corrected text proposed by the grader; ``None`` when absent.
    """

    ok: bool
    issues: tuple[str, ...] = field(default_factory=tuple)
    corrected_text: str | None = None

    def _validate(self) -> None:
        if any(not issue for issue in self.issues):
            message = "Grader issues must not contain empty entries."
            raise ValidationError(message)


__all__ = ("GradeVerdict",)
