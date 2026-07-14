"""add locale and translations to analyses and opportunities

Revision ID: 005
Revises: 004
Create Date: 2026-07-14

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "005_locale_translations"
down_revision: Union[str, None] = "004_job_runs"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "analyses",
        sa.Column("locale", sa.String(length=16), nullable=False, server_default="zh-CN"),
    )
    op.add_column(
        "analyses",
        sa.Column("translations", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.add_column(
        "opportunities",
        sa.Column("locale", sa.String(length=16), nullable=False, server_default="zh-CN"),
    )
    op.add_column(
        "opportunities",
        sa.Column("translations", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("opportunities", "translations")
    op.drop_column("opportunities", "locale")
    op.drop_column("analyses", "translations")
    op.drop_column("analyses", "locale")
