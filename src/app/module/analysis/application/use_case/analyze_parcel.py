"""Analyze parcel use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import AnalyzeParcelCommand
from app.module.analysis.application.dto.response import ParcelAnalysisResponse
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.analysis.application.port import (
        ClimateProvider,
        InfrastructureProvider,
        TopographyProvider,
    )


class AnalyzeParcelUseCase(BaseUseCase[AnalyzeParcelCommand, ParcelAnalysisResponse]):
    """Aggregate all parcel metrics into a single result.

    Calculates metrics through the Topography, Infrastructure and Climate
    provider ports and composes them into one response.

    MVP: infrastructure categories and their buffer radii are hardcoded here.
    Later they may come from the request (per-module analysis settings).
    """

    # Default infrastructure categories with buffer radii (meters).
    _INFRASTRUCTURE_CATEGORIES: tuple[tuple[str, int], ...] = (
        ("school", 1000),
        ("hospital", 2000),
        ("shop", 500),
        ("transit_stop", 500),
        ("water_body", 2000),
    )

    def __init__(
        self,
        topography_provider: TopographyProvider,
        infrastructure_provider: InfrastructureProvider,
        climate_provider: ClimateProvider,
    ) -> None:
        self._topography_provider = topography_provider
        self._infrastructure_provider = infrastructure_provider
        self._climate_provider = climate_provider
        self._logger = get_logger("app.analysis.use_case.analyze_parcel")

    @override
    async def __call__(self, command: AnalyzeParcelCommand) -> ParcelAnalysisResponse:
        self._logger.info("Analyzing parcel: parcel_id=%s", command.parcel_id)

        topography = await self._topography_provider.calculate_parcel_metrics(
            command.parcel_id,
            command.current_user_id,
        )
        infrastructure = await self._infrastructure_provider.calculate_parcel_metrics(
            command.parcel_id,
            command.current_user_id,
            list(self._INFRASTRUCTURE_CATEGORIES),
        )
        climate = await self._climate_provider.calculate_parcel_metrics(
            command.parcel_id,
            command.current_user_id,
        )

        self._logger.info("Parcel metrics aggregated: parcel_id=%s", command.parcel_id)

        return ParcelAnalysisResponse(
            parcel_id=command.parcel_id,
            topography=topography,
            infrastructure=infrastructure,
            climate=climate,
        )


__all__ = ("AnalyzeParcelUseCase",)
