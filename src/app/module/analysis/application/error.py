"""Analysis module application errors."""

from app.module.shared.application.error import ApplicationError


class AnalysisNotFoundError(ApplicationError):
    """Raised when an analysis is not found or not accessible to the user."""

    def __init__(self, analysis_id: str) -> None:
        super().__init__(f"Analysis '{analysis_id}' not found.")


class AnalysisNotDeletableError(ApplicationError):
    """Raised when an analysis cannot be deleted in its current status."""

    def __init__(self, status: str) -> None:
        super().__init__(f"Analysis cannot be deleted while it is '{status}'.")


__all__ = ("AnalysisNotDeletableError", "AnalysisNotFoundError")
