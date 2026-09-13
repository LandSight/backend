"""Analysis HTTP endpoints."""

from __future__ import annotations

from uuid import UUID

from litestar import get, post
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK, HTTP_202_ACCEPTED

from app.interface.http.schema.analysis import AnalysisResponse, StartAnalysisRequest
from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.util.guards import require_authorization
from app.module.analysis.interface.internal.dto import (
    AnalysisResult,
    GetAnalysisInput,
    ListUserAnalysesInput,
    StartAnalysisInput,
)
from app.module.analysis.interface.internal.port import AnalysisInternalAPI


class AnalysisController(Controller):
    """Analysis endpoints."""

    path = "/"
    tags = ("analysis",)
    guards = [require_authorization]

    @post(
        "/",
        status_code=HTTP_202_ACCEPTED,
        description="Start an analysis for a parcel.",
    )
    async def start_analysis(
        self,
        data: StartAnalysisRequest,
        analysis_api: AnalysisInternalAPI,
        current_user: CurrentUser,
    ) -> AnalysisResponse:
        """Start an analysis for a parcel."""
        result = await analysis_api.start_analysis(
            StartAnalysisInput(
                parcel_id=data.parcel_id,
                current_user_id=current_user.id,
                name=data.name,
            ),
        )
        return self._to_schema(result)

    @get(
        "/",
        status_code=HTTP_200_OK,
        description="List all analyses of the current user across all statuses.",
    )
    async def list_user_analyses(
        self,
        analysis_api: AnalysisInternalAPI,
        current_user: CurrentUser,
    ) -> list[AnalysisResponse]:
        """List all analyses of the current user."""
        results = await analysis_api.list_user_analyses(
            ListUserAnalysesInput(current_user_id=current_user.id),
        )
        return [self._to_schema(result) for result in results]

    @get(
        "/{analysis_id:uuid}",
        status_code=HTTP_200_OK,
        description="Get an analysis by its ID.",
    )
    async def get_analysis(
        self,
        analysis_id: UUID,
        analysis_api: AnalysisInternalAPI,
        current_user: CurrentUser,
    ) -> AnalysisResponse:
        """Get an analysis by its ID."""
        result = await analysis_api.get_analysis(
            GetAnalysisInput(analysis_id=analysis_id, current_user_id=current_user.id),
        )
        return self._to_schema(result)

    @staticmethod
    def _to_schema(result: AnalysisResult) -> AnalysisResponse:
        """Map an internal result DTO to the HTTP response schema."""
        return AnalysisResponse(
            id=result.id,
            parcel_id=result.parcel_id,
            name=result.name,
            status=result.status,
            score=result.score,
            status_reason=result.status_reason,
            created_at=result.created_at,
        )


__all__ = ("AnalysisController",)
