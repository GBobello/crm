"""Creating superuser field to user.

Revision ID: 50aadbc7d18d
Revises: 82dd2e9d8139
Create Date: 2025-04-19 09:52:03.265949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50aadbc7d18d'
down_revision: Union[str, None] = '82dd2e9d8139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'is_superuser')
