"""Your migration message

Revision ID: 20fbac2ace3b
Revises: e97f15811643
Create Date: 2025-02-17 15:55:04.974616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20fbac2ace3b'
down_revision: Union[str, None] = 'e97f15811643'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
