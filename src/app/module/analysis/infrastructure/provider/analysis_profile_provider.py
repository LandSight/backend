"""Analysis profile provider backed by the packaged profile configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import AnalysisProfileProvider
from app.module.analysis.domain.value_object import (
    AnalysisProfile,
    AnalysisProfileDescription,
    AnalysisProfileName,
)
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.analysis.domain.value_object import AnalysisType
    from app.module.analysis.infrastructure.config.models import AnalysisProfilesConfig


class AnalysisProfileProviderImpl(AnalysisProfileProvider):
    """Resolve catalog entries and collection parameters from the configuration."""

    def __init__(self, config: AnalysisProfilesConfig) -> None:
        self._profiles = config.profiles

    @override
    def list_profiles(self) -> tuple[AnalysisProfile, ...]:
        """See :class:`app.module.analysis.application.port.AnalysisProfileProvider.list_profiles`."""
        return tuple(
            AnalysisProfile(
                key=key,
                name=AnalysisProfileName(profile.name),
                description=AnalysisProfileDescription(profile.description),
            )
            for key, profile in self._profiles.items()
        )

    @override
    def infrastructure_buffers(self, analysis_type: AnalysisType) -> Mapping[str, int]:
        """See :class:`app.module.analysis.application.port.AnalysisProfileProvider.infrastructure_buffers`."""
        profile = self._profiles.get(analysis_type)
        if profile is None:
            message = f"No analysis profile configured for analysis type '{analysis_type}'."
            raise ValidationError(message)
        return profile.infrastructure.buffers


__all__ = ("AnalysisProfileProviderImpl",)
