"""Your migration message

Revision ID: d9a358cfc12a
Revises: 20fbac2ace3b
Create Date: 2025-02-17 15:58:42.612706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9a358cfc12a'
down_revision: Union[str, None] = '20fbac2ace3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
