"""Restriction module application errors."""

from __future__ import annotations

from app.module.shared.application.error import ApplicationError


class RestrictionZonesNotLoadedError(ApplicationError):
    """Raised when the restriction zones have not been built yet.

    An empty zone table would report every parcel as unrestricted, so the
    check refuses to run instead.
    """

    def __init__(self) -> None:
        super().__init__("Restriction zones are not loaded; run the restriction zone ETL first.")


class RestrictionCheckNotFoundError(ApplicationError):
    """Raised when a restriction check is not found."""

    def __init__(self, check_id: str) -> None:
        super().__init__(f"Restriction check with id '{check_id}' not found.")


__all__ = ("RestrictionCheckNotFoundError", "RestrictionZonesNotLoadedError")
