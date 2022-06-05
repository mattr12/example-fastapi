"""add content column to posts table

Revision ID: 46f3a9a220a4
Revises: 3d04e6b26ba9
Create Date: 2022-06-05 19:32:36.327568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "46f3a9a220a4"
down_revision = "3d04e6b26ba9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
