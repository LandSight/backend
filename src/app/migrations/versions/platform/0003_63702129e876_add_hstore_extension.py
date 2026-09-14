"""Add hstore extension.

Revision ID: 63702129e876
Revises: ef70c85c6229
Create Date: 2026-09-05 16:32:25.688973

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "63702129e876"
down_revision: str | Sequence[str] | None = "ef70c85c6229"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Enable hstore extension. It is required by the ``tags`` columns of the
    # ``infrastructure.planet_osm_point`` / ``planet_osm_polygon`` layers created
    # by ``osm2pgsql`` and read by the Infrastructure module.
    op.execute("CREATE EXTENSION IF NOT EXISTS hstore")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP EXTENSION IF EXISTS hstore")
