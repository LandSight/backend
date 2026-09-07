"""Analysis HTTP endpoints."""

from __future__ import annotations

import dataclasses
from uuid import UUID

from litestar import post
from litestar.controller import Controller
from litestar.status_codes import HTTP_201_CREATED

from app.interface.http.schema.analysis import ParcelAnalysisResponse
from app.interface.http.schema.climate import ClimateMetricsResponse
from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.schema.infrastructure import InfrastructureMetricsResponse
from app.interface.http.schema.topography import TopographyMetricsResponse
from app.interface.http.util.guards import require_authorization
from app.module.analysis.interface.internal.dto import AnalyzeParcelInput, ParcelAnalysisResult
from app.module.analysis.interface.internal.port import AnalysisInternalAPI


class AnalysisController(Controller):
    """Analysis endpoints."""

    path = "/"
    tags = ("analysis",)
    guards = [require_authorization]

    @post(
        "/{parcel_id:uuid}",
        status_code=HTTP_201_CREATED,
        description=(
            "Run a parcel analysis: recalculates topography, infrastructure and "
            "climate metrics and returns them aggregated."
        ),
    )
    async def analyze_parcel(
        self,
        parcel_id: UUID,
        analysis_api: AnalysisInternalAPI,
        current_user: CurrentUser,
    ) -> ParcelAnalysisResponse:
        """Run a parcel analysis and return the aggregated metrics."""
        result = await analysis_api.analyze_parcel(
            AnalyzeParcelInput(parcel_id=parcel_id, current_user_id=current_user.id),
        )
        return self._to_schema(result)

    @staticmethod
    def _to_schema(result: ParcelAnalysisResult) -> ParcelAnalysisResponse:
        """Map an internal result DTO to the HTTP response schema."""
        return ParcelAnalysisResponse(
            parcel_id=result.parcel_id,
            topography=TopographyMetricsResponse(**dataclasses.asdict(result.topography)),
            infrastructure=InfrastructureMetricsResponse(**dataclasses.asdict(result.infrastructure)),
            climate=ClimateMetricsResponse(**dataclasses.asdict(result.climate)),
        )


__all__ = ("AnalysisController",)
