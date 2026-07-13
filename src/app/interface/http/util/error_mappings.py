"""Error mappings assembly for the application."""

from app.module.identity.error_mappings import (
    get_identity_application_error_mappings,
    get_identity_domain_error_mappings,
)
from app.module.shared.interface.http.error_mappings import (
    get_shared_application_error_mappings,
    get_shared_domain_error_mappings,
)


def get_all_domain_error_mappings() -> dict:
    """Merge all domain error mappings.

    Returns
    -------
    dict
        Combined domain error mappings.
    """
    mappings = {}
    mappings.update(get_shared_domain_error_mappings())
    mappings.update(get_identity_domain_error_mappings())
    return mappings


def get_all_application_error_mappings() -> dict:
    """Merge all application error mappings.

    Returns
    -------
    dict
        Combined application error mappings.
    """
    mappings = {}
    mappings.update(get_shared_application_error_mappings())
    mappings.update(get_identity_application_error_mappings())
    return mappings
