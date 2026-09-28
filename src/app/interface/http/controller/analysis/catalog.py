"""Analysis catalog HTTP endpoints: profiles and engines."""

from __future__ import annotations

from litestar import Controller, get
from litestar.status_codes import HTTP_200_OK

from app.interface.http.schema.analysis import (
    EngineSchema,
    EnginesResponse,
    ProfileSchema,
    ProfilesResponse,
)
from app.interface.http.util.guards import require_authorization
from app.module.analysis.application.port import AnalysisProfileProvider, EngineProvider


class AnalysisCatalogController(Controller):
    """Read-only catalog endpoints used by the analysis start form."""

    path = "/"
    tags = ("analysis",)
    guards = [require_authorization]

    @get(
        "/profiles",
        status_code=HTTP_200_OK,
        description="List the available analysis profiles.",
    )
    async def list_profiles(self, analysis_profiles: AnalysisProfileProvider) -> ProfilesResponse:
        """List the available analysis profiles."""
        return ProfilesResponse(
            profiles=[
                ProfileSchema(
                    key=profile.key.value,
                    name=profile.name.unwrap(),
                    description=profile.description.unwrap(),
                )
                for profile in analysis_profiles.list_profiles()
            ],
        )

    @get(
        "/engines",
        status_code=HTTP_200_OK,
        description="List the available scoring engines.",
    )
    async def list_engines(self, engine_provider: EngineProvider) -> EnginesResponse:
        """List the available scoring engines."""
        return EnginesResponse(
            engines=[
                EngineSchema(
                    key=engine.key.value,
                    name=engine.name.unwrap(),
                    description=engine.description.unwrap(),
                    version=engine.version,
                )
                for engine in engine_provider.list_engines()
            ],
        )


__all__ = ("AnalysisCatalogController",)
