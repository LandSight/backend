"""Dependency injection for Analysis module."""

from litestar.di import NamedDependency, Provide

from app.module.analysis.application.use_case import AnalyzeParcelUseCase
from app.module.analysis.infrastructure.provider import (
    ClimateProviderImpl,
    InfrastructureProviderImpl,
    TopographyProviderImpl,
)
from app.module.analysis.interface.internal.api import AnalysisInternal
from app.module.climate.interface.internal.port import ClimateInternalAPI
from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI
from app.module.topography.interface.internal.port import TopographyInternalAPI


# ----- Providers -----
def provide_topography_provider(
    topography_api: NamedDependency[TopographyInternalAPI],
) -> TopographyProviderImpl:
    return TopographyProviderImpl(topography_api)


def provide_infrastructure_provider(
    infrastructure_api: NamedDependency[InfrastructureInternalAPI],
) -> InfrastructureProviderImpl:
    return InfrastructureProviderImpl(infrastructure_api)


def provide_climate_provider(
    climate_api: NamedDependency[ClimateInternalAPI],
) -> ClimateProviderImpl:
    return ClimateProviderImpl(climate_api)


# ----- Use Cases -----
def provide_analyze_parcel_use_case(
    analysis_topography_provider: NamedDependency[TopographyProviderImpl],
    analysis_infrastructure_provider: NamedDependency[InfrastructureProviderImpl],
    analysis_climate_provider: NamedDependency[ClimateProviderImpl],
) -> AnalyzeParcelUseCase:
    return AnalyzeParcelUseCase(
        topography_provider=analysis_topography_provider,
        infrastructure_provider=analysis_infrastructure_provider,
        climate_provider=analysis_climate_provider,
    )


# ----- Internal API -----
def provide_analysis_internal(
    analyze_parcel_use_case: NamedDependency[AnalyzeParcelUseCase],
) -> AnalysisInternal:
    return AnalysisInternal(analyze_parcel_use_case=analyze_parcel_use_case)


analysis_dependencies = {
    "analysis_topography_provider": Provide(provide_topography_provider, sync_to_thread=False),
    "analysis_infrastructure_provider": Provide(provide_infrastructure_provider, sync_to_thread=False),
    "analysis_climate_provider": Provide(provide_climate_provider, sync_to_thread=False),
    "analyze_parcel_use_case": Provide(provide_analyze_parcel_use_case, sync_to_thread=False),
    "analysis_api": Provide(provide_analysis_internal, sync_to_thread=False),
}

__all__ = ("analysis_dependencies",)
