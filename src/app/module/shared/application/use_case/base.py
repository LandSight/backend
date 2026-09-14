from abc import ABC, abstractmethod


class BaseUseCase[CommandT, ResultT](ABC):
    """Base class for all use cases."""

    @abstractmethod
    async def __call__(self, command: CommandT) -> ResultT:
        """Execute the use case with the given command."""
        raise NotImplementedError


__all__ = ("BaseUseCase",)
