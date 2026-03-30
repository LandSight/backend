from typing import override

from app.module.shared.application.use_case.base import BaseUseCase


class DummyUseCase(BaseUseCase[int, str]):
    """Dummy use case for testing."""

    @override
    async def __call__(self, command: int) -> str:
        return str(command)


class TestBaseUseCase:
    """Test cases for the BaseUseCase class."""

    async def test_concrete_implementation_works(self) -> None:
        """Should work when properly implemented."""
        use_case = DummyUseCase()
        result = await use_case(1)
        assert result == "1"
