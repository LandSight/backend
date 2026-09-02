"""Create ci_text collation.

Revision ID: fd780af9c921
Revises:
Create Date: 2026-07-13 11:53:29.788553

"""

from typing import TYPE_CHECKING

from alembic import op

from app.platform.constants import COLLATION_CI_TEXT_NAME


if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "fd780af9c921"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        f"CREATE COLLATION IF NOT EXISTS {COLLATION_CI_TEXT_NAME} ("
        "    provider = icu,"
        "    locale = 'und-u-ks-level2',"
        "    deterministic = false"
        ")"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(f"DROP COLLATION IF EXISTS {COLLATION_CI_TEXT_NAME}")
