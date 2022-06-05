"""create basic post table

Revision ID: 3d04e6b26ba9
Revises: 
Create Date: 2022-06-05 19:20:27.214595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3d04e6b26ba9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("title", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("posts")
