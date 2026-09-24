"""Get analysis metrics command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetAnalysisMetricsCommand:
    """Command for retrieving the metric references of an analysis.

    Attributes
    ----------
    analysis_id : UUID
        ID of the analysis whose metric references to retrieve.
    current_user_id : UUID
        ID of the user performing the request.
    module : str | None
        Optional metric module filter (e.g. ``infrastructure``); ``None``
        returns references from every module.
    """

    analysis_id: UUID
    current_user_id: UUID
    module: str | None = None


__all__ = ("GetAnalysisMetricsCommand",)
