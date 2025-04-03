"""Creating lawyer model

Revision ID: edb2e7a15641
Revises: cbf163eb473e
Create Date: 2025-04-02 23:32:54.852488

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "edb2e7a15641"
down_revision: Union[str, None] = "cbf163eb473e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "lawyers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("document", sa.String(length=14), nullable=False),
        sa.Column("phone", sa.String(length=15), nullable=False),
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
        sa.Column("photo_url", sa.String(), nullable=True),
        sa.Column("oab", sa.String(), nullable=False),
        sa.Column(
            "oab_state",
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
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("lawyers")
