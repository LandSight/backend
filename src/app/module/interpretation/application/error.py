"""Interpretation application errors."""

from app.module.shared.application.error import ApplicationError


class InterpretationNotAvailableError(ApplicationError):
    """Raised when an analysis has no stored interpretation report yet."""

    def __init__(self, analysis_id: str) -> None:
        super().__init__(f"Interpretation for analysis '{analysis_id}' is not available.")


__all__ = ("InterpretationNotAvailableError",)
