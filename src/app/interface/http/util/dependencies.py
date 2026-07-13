"""Dependency assembly for the application."""

from typing import TYPE_CHECKING

from app.module.identity.di import identity_dependencies
from app.platform.di import platform_dependencies


if TYPE_CHECKING:
    from litestar.di import Provide


def get_all_dependencies() -> dict[str, Provide]:
    """Merge all module dependencies into a single dictionary.

    Returns
    -------
    dict[str, Provide]
        Combined dependencies dictionary.
    """
    dependencies = {}
    dependencies.update(platform_dependencies)
    dependencies.update(identity_dependencies)
    return dependencies
