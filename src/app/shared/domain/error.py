class DomainError(Exception):
    """Base class for all domain errors."""


class ValidationError(DomainError):
    """Validation domain error."""
