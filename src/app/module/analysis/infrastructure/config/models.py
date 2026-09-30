"""Pydantic models for the analysis profiles configuration.

Profiles are keyed by analysis type and own the metric-collection parameters
that are independent of the scoring engine, such as the infrastructure search
buffers. The scoring configuration (hierarchy, fuzzy functions) stays in the
engine configuration.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.module.analysis.domain.value_object import AnalysisType  # noqa: TC001 - needed at runtime for pydantic


_BUFFER_MIN_METERS = 1
_BUFFER_MAX_METERS = 200_000

# ``Buffer`` in the infrastructure module shares these bounds. Keeping a local
# alias avoids an application-to-module domain dependency.
BufferMeters = Annotated[int, Field(ge=_BUFFER_MIN_METERS, le=_BUFFER_MAX_METERS)]


class InfrastructureCollectionConfig(BaseModel):
    """Infrastructure metric-collection parameters of a profile.

    Attributes
    ----------
    buffers : dict[str, BufferMeters]
        Search radius in meters per infrastructure category key.
    """

    model_config = ConfigDict(extra="forbid")

    buffers: dict[str, BufferMeters] = Field(default_factory=dict)


class AnalysisProfileConfig(BaseModel):
    """Collection and catalog configuration of a single analysis profile.

    Attributes
    ----------
    name : str
        Display name of the profile, shown in the profile catalogue.
    description : str
        Human-readable description of what the profile evaluates.
    infrastructure : InfrastructureCollectionConfig
        Infrastructure metric-collection parameters.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=64)
    description: str = Field(min_length=1, max_length=256)
    infrastructure: InfrastructureCollectionConfig = Field(default_factory=InfrastructureCollectionConfig)


class AnalysisProfilesConfig(BaseModel):
    """Root configuration keyed by analysis type."""

    model_config = ConfigDict(extra="forbid")

    profiles: dict[AnalysisType, AnalysisProfileConfig] = Field(min_length=1)


__all__ = (
    "AnalysisProfileConfig",
    "AnalysisProfilesConfig",
    "BufferMeters",
    "InfrastructureCollectionConfig",
)
