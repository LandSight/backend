"""Add restriction check hits table.

One row per zone kind overlapping the parcel of a check.

Revision ID: 15c5b262d419
Revises: 762d8b5871fa
Create Date: 2026-10-16 10:00:01.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "15c5b262d419"
down_revision: str | Sequence[str] | None = "762d8b5871fa"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "check_hits",
        sa.Column("check_id", sa.UUID(), nullable=False, comment="ID of the restriction check"),
        sa.Column("position", sa.Integer(), nullable=False, comment="Order of the hit within the check"),
        sa.Column("kind", sa.String(length=64), nullable=False, comment="Zone kind, see RestrictionKind"),
        sa.Column(
            "overlap_area_m2",
            sa.Float(),
            nullable=False,
            comment="Area of the parcel inside the zones in square meters",
        ),
        sa.Column(
            "overlap_share", sa.Float(), nullable=False, comment="Share of the parcel area inside the zones, 0..1"
        ),
        sa.Column(
            "zone_names", postgresql.ARRAY(sa.Text()), nullable=False, comment="Names of the source objects, when known"
        ),
        sa.Column(
            "legal_basis", sa.Text(), nullable=False, comment="Short reference to the rule that defines the zone"
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["check_id"],
            ["restriction.checks.id"],
            name=op.f("fk_check_hits_check_id_checks"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_check_hits")),
        schema="restriction",
    )
    op.create_index(
        op.f("ix_restriction_check_hits_check_id"), "check_hits", ["check_id"], unique=False, schema="restriction"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_restriction_check_hits_check_id"), table_name="check_hits", schema="restriction")
    op.drop_table("check_hits", schema="restriction")
