"""Add applied constraints.

Evaluations keep the multi-criteria score before the restriction zones were
applied, and the zones that barred the scenario or lowered the score.

Revision ID: fcaa4832215f
Revises: d7e8f9a0b1c2
Create Date: 2026-10-12 12:16:35.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "fcaa4832215f"
down_revision: str | Sequence[str] | None = "d7e8f9a0b1c2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "analysis_evaluations",
        sa.Column(
            "base_score",
            sa.Float(),
            nullable=True,
            comment="Score of the multi-criteria breakdown before the constraints; NULL before constraints existed",
        ),
        schema="analysis",
    )
    op.alter_column(
        "analysis_evaluations",
        "total_score",
        existing_type=sa.Float(),
        comment="Final score on the 0-10 scale, after the constraints",
        existing_comment="Final score on the 0-10 scale",
        existing_nullable=False,
        schema="analysis",
    )
    op.create_table(
        "analysis_applied_constraints",
        sa.Column("evaluation_id", sa.UUID(), nullable=False, comment="ID of the owning evaluation"),
        sa.Column("position", sa.Integer(), nullable=False, comment="Order of the constraint within the evaluation"),
        sa.Column("kind", sa.String(length=64), nullable=False, comment="Restriction zone kind"),
        sa.Column("effect", sa.String(length=16), nullable=False, comment="prohibit or penalty"),
        sa.Column("factor", sa.Float(), nullable=False, comment="Multiplier applied to the score"),
        sa.Column("overlap_share", sa.Float(), nullable=False, comment="Share of the parcel inside the zone, 0..1"),
        sa.Column(
            "overlap_area_m2",
            sa.Float(),
            nullable=False,
            comment="Area of the parcel inside the zone in square meters",
        ),
        sa.Column(
            "zone_names", postgresql.ARRAY(sa.Text()), nullable=False, comment="Names of the source objects, when known"
        ),
        sa.Column(
            "legal_basis", sa.Text(), nullable=False, comment="Short reference to the rule that defines the zone"
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["evaluation_id"],
            ["analysis.analysis_evaluations.id"],
            name=op.f("fk_analysis_applied_constraints_evaluation_id_analysis_evaluations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analysis_applied_constraints")),
        schema="analysis",
    )
    op.create_index(
        "ix_analysis_applied_constraints_evaluation_id",
        "analysis_applied_constraints",
        ["evaluation_id"],
        unique=False,
        schema="analysis",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "ix_analysis_applied_constraints_evaluation_id", table_name="analysis_applied_constraints", schema="analysis"
    )
    op.drop_table("analysis_applied_constraints", schema="analysis")
    op.alter_column(
        "analysis_evaluations",
        "total_score",
        existing_type=sa.Float(),
        comment="Final score on the 0-10 scale",
        existing_comment="Final score on the 0-10 scale, after the constraints",
        existing_nullable=False,
        schema="analysis",
    )
    op.drop_column("analysis_evaluations", "base_score", schema="analysis")
