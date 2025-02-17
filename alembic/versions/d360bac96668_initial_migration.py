"""Initial migration

Revision ID: d360bac96668
Revises: 9f4d4811e46d
Create Date: 2025-02-17 15:42:37.519074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd360bac96668'
down_revision: Union[str, None] = '9f4d4811e46d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
