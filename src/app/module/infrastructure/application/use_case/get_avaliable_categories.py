"""Get available infrastructure categories use case."""

from __future__ import annotations

from typing import override

from app.module.infrastructure.application.dto.response import CategoryInfoResponse
from app.module.infrastructure.domain.value_object import Category
from app.module.shared.application.use_case import BaseUseCase


class GetAvailableCategoriesUseCase(BaseUseCase[None, list[CategoryInfoResponse]]):
    """Get list of all available infrastructure categories."""

    @override
    async def __call__(self, command: None = None) -> list[CategoryInfoResponse]:
        return [CategoryInfoResponse(category=category.value) for category in Category]


__all__ = ("GetAvailableCategoriesUseCase",)
