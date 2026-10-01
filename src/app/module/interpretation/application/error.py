"""Interpretation application errors."""

from app.module.shared.application.error import ApplicationError


class InterpretationNotAvailableError(ApplicationError):
    """Raised when an analysis has no stored interpretation report yet."""

    def __init__(self, analysis_id: str) -> None:
        super().__init__(f"Interpretation for analysis '{analysis_id}' is not available.")


class InterpretationGenerationError(ApplicationError):
    """Raised when the configured generation strategy cannot produce a report.

    The error belongs to the application contract of the interpreter: any
    backing implementation (an LLM, a template, ...) that fails to generate text
    raises it, so the interpreter can fall back to safe text. The cause is
    carried in the message.
    """

    def __init__(self, reason: str) -> None:
        super().__init__(f"Failed to generate the interpretation report: {reason}")


__all__ = ("InterpretationGenerationError", "InterpretationNotAvailableError")
