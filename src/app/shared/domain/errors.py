class DomainError(Exception):
    """Base class for domain-specific errors."""


class InvalidUUIDTypeError(DomainError):
    """Raised when a value is not a valid UUID instance."""

    def __init__(self, value: object) -> None:
        super().__init__(f"Invalid UUID: {value}")


class InvalidUUIDVersionError(DomainError):
    """Raised when a UUID has an incorrect version."""

    def __init__(self, version: int | None) -> None:
        super().__init__(f"Invalid UUID version: {version}")
