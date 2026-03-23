class DomainError(Exception):
    """Base class for all domain errors."""


class ValidationError(DomainError):
    """Validation domain error."""


class InvalidEntityIdError(ValidationError):
    """Invalid entity ID error."""
