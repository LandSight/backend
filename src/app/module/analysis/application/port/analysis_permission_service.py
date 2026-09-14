"""Analysis permission service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


class AnalysisPermissionService(ABC):
    """Port for checking access to a parcel's analysis.

    Implementations:
    - :class:`app.module.analysis.infrastructure.permission.analysis_permission_service.AnalysisPermissionServiceImpl`
    """

    @abstractmethod
    async def user_can_view_parcel(self, user_id: UUID, parcel_id: UUID) -> bool:
        """Return whether the user may view analyses for the parcel.

        Parameters
        ----------
        user_id : UUID
            ID of the user performing the request.
        parcel_id : UUID
            ID of the parcel.

        Returns
        -------
        bool
            ``True`` if access is granted, ``False`` otherwise.
        """
        raise NotImplementedError


__all__ = ("AnalysisPermissionService",)
