"""Analysis profile provider port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.analysis.domain.value_object import AnalysisType


class AnalysisProfileProvider(ABC):
    """Port for resolving profile-scoped metric-collection parameters.

    A profile is selected by analysis type and owns the parameters that define
    how metrics are collected, independently of the scoring engine.

    Implementations:
    - :class:`app.module.analysis.infrastructure.config.analysis_profile_provider.AnalysisProfileProviderImpl`
    """

    @abstractmethod
    def infrastructure_buffers(self, analysis_type: AnalysisType) -> Mapping[str, int]:
        """Return infrastructure search buffers in meters for the profile.

        Parameters
        ----------
        analysis_type : AnalysisType
            Evaluation profile whose collection parameters are requested.

        Returns
        -------
        Mapping[str, int]
            Buffer radius in meters per infrastructure category key.
        """
        raise NotImplementedError


__all__ = ("AnalysisProfileProvider",)
