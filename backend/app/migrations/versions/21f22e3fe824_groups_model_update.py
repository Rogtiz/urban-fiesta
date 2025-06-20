"""Groups model update

Revision ID: 21f22e3fe824
Revises: 6bfc18cdc830
Create Date: 2025-04-16 22:12:21.458543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21f22e3fe824'
down_revision: Union[str, None] = '6bfc18cdc830'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'groups', 'users', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_column('groups', 'owner_id')
    # ### end Alembic commands ###
