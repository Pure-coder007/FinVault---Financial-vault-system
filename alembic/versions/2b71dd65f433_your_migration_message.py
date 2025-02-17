"""Your migration message

Revision ID: 2b71dd65f433
Revises: d9a358cfc12a
Create Date: 2025-02-17 16:00:18.935877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b71dd65f433'
down_revision: Union[str, None] = 'd9a358cfc12a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
