"""Concrete implementation of the Analysis module's internal API.

See :class:`app.module.analysis.interface.internal.port.AnalysisInternalAPI`
for the abstract interface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.dto.command import AnalyzeParcelCommand
from app.module.analysis.interface.internal.dto import AnalyzeParcelInput, ParcelAnalysisResult
from app.module.analysis.interface.internal.port import AnalysisInternalAPI


if TYPE_CHECKING:
    from app.module.analysis.application.dto.response import ParcelAnalysisResponse
    from app.module.analysis.application.use_case import AnalyzeParcelUseCase


class AnalysisInternal(AnalysisInternalAPI):
    """Concrete implementation of the Analysis internal API.

    Wraps the application-layer use case into a single cohesive interface that
    the HTTP layer calls.
    """

    def __init__(self, analyze_parcel_use_case: AnalyzeParcelUseCase) -> None:
        self._analyze_parcel = analyze_parcel_use_case

    @override
    async def analyze_parcel(self, input_data: AnalyzeParcelInput) -> ParcelAnalysisResult:
        """See :meth:`AnalysisInternalAPI.analyze_parcel`."""
        result = await self._analyze_parcel(
            AnalyzeParcelCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self._to_result(result)

    @staticmethod
    def _to_result(result: ParcelAnalysisResponse) -> ParcelAnalysisResult:
        """Map an application response DTO to an internal result DTO."""
        return ParcelAnalysisResult(
            parcel_id=result.parcel_id,
            topography=result.topography,
            infrastructure=result.infrastructure,
            climate=result.climate,
        )


__all__ = ("AnalysisInternal",)
