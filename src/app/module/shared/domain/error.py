class DomainError(Exception):
    """Base class for domain errors."""


class ValidationError(DomainError):
    """Raised when a value fails validation."""


__all__ = (
    "DomainError",
    "ValidationError",
)
