class DomainError(Exception):
    """Base class for domain errors."""


class InvariantViolationError(DomainError):
    """Raised when an entity's invariant is violated."""


class ValidationError(DomainError):
    """Raised when a value fails validation."""


__all__ = (
    "DomainError",
    "InvariantViolationError",
    "ValidationError",
)
