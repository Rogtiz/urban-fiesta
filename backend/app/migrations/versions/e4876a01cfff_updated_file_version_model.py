"""updated file version model

Revision ID: e4876a01cfff
Revises: 41ca7eb7f378
Create Date: 2025-06-16 15:13:24.299965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4876a01cfff'
down_revision: Union[str, None] = '41ca7eb7f378'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file_versions', sa.Column('path', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('file_versions', 'path')
    # ### end Alembic commands ###
