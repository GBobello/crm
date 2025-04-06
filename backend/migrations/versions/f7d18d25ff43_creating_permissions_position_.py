"""creating permissions, position permissions and linking with user the position

Revision ID: f7d18d25ff43
Revises: 8558fdd9e0b3
Create Date: 2025-04-06 14:03:05.568504

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f7d18d25ff43"
down_revision: Union[str, None] = "8558fdd9e0b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "positions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "position_permissions",
        sa.Column("position_id", sa.Integer(), nullable=True),
        sa.Column("permission_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["permissions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["position_id"],
            ["positions.id"],
        ),
    )
    op.add_column("users", sa.Column("position_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_user_position_id", "users", "positions", ["position_id"], ["id"]
    )


def downgrade() -> None:
    op.drop_constraint("fk_user_position_id", "users", type_="foreignkey")
    op.drop_column("users", "position_id")
    op.drop_table("position_permissions")
    op.drop_table("positions")
    op.drop_table("permissions")
