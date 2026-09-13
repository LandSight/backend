"""Analysis module application errors."""

from app.module.shared.application.error import ApplicationError


class AnalysisNotFoundError(ApplicationError):
    """Raised when an analysis is not found or not accessible to the user."""

    def __init__(self, analysis_id: str) -> None:
        super().__init__(f"Analysis '{analysis_id}' not found.")


__all__ = ("AnalysisNotFoundError",)
