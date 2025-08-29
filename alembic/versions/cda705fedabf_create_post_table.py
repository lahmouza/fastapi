"""create_post_table

Revision ID: cda705fedabf
Revises: 
Create Date: 2025-08-28 18:40:06.763665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cda705fedabf'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, index=True, nullable=False),
        sa.Column('title', sa.String, index=True, nullable=False)
    )
    op.add_column('posts', sa.Column('content', sa.String, index=True, nullable=False))

    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    op.drop_column('posts', 'content')
    
