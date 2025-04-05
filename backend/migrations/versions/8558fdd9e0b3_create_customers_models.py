"""create customers models

Revision ID: 8558fdd9e0b3
Revises: edb2e7a15641
Create Date: 2025-04-05 01:19:05.990414

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8558fdd9e0b3"
down_revision: Union[str, None] = "edb2e7a15641"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("document", sa.String(length=14), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=15), nullable=False),
        sa.Column("created_date", sa.Date(), nullable=True),
        sa.Column("born_date", sa.Date(), nullable=False),
        sa.Column(
            "civil_status",
            sa.Enum(
                "SOLTEIRO",
                "CASADO",
                "DIVORCIADO",
                "VIUVO",
                "SEPARADO_JUDICIALMENTE",
                "UNIAO_ESTAVEL",
                "OUTRO",
                name="civilstatus",
            ),
            nullable=True,
        ),
        sa.Column("address", sa.String(length=200), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column(
            "state",
            sa.Enum(
                "AC",
                "AL",
                "AP",
                "AM",
                "BA",
                "CE",
                "DF",
                "ES",
                "GO",
                "MA",
                "MT",
                "MS",
                "MG",
                "PA",
                "PB",
                "PR",
                "PE",
                "PI",
                "RJ",
                "RN",
                "RS",
                "RO",
                "RR",
                "SC",
                "SP",
                "SE",
                "TO",
                name="state",
            ),
            nullable=True,
        ),
        sa.Column("zip_code", sa.String(length=10), nullable=True),
        sa.Column("country", sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_customers_id"), "customers", ["id"], unique=False)


def downgrade() -> None:
    op.alter_column(
        "sessions",
        "id",
        existing_type=sa.UUID(),
        type_=sa.NUMERIC(),
        existing_nullable=False,
    )
    op.drop_index(op.f("ix_customers_id"), table_name="customers")
    op.drop_table("customers")
