"""Analysis profiles configuration (collection parameters per analysis type)."""

from __future__ import annotations

from .analysis_profile_provider import AnalysisProfileProviderImpl
from .loader import load_analysis_profiles
from .models import AnalysisProfileConfig, AnalysisProfilesConfig, InfrastructureCollectionConfig


__all__ = (
    "AnalysisProfileConfig",
    "AnalysisProfileProviderImpl",
    "AnalysisProfilesConfig",
    "InfrastructureCollectionConfig",
    "load_analysis_profiles",
)
