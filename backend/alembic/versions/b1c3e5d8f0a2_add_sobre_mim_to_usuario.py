"""add sobre_mim to usuario

Revision ID: b1c3e5d8f0a2
Revises: 4143e2bdf2eb
Create Date: 2026-10-14 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1c3e5d8f0a2"
down_revision: Union[str, Sequence[str], None] = "4143e2bdf2eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("usuario", sa.Column("sobre_mim", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("usuario", "sobre_mim")
