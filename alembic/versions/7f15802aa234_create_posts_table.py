"""create posts table

Revision ID: 7f15802aa234
Revises: 
Create Date: 2021-12-16 18:04:50.883441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f15802aa234'
down_revision = None
branch_labels = None
depends_on = None


# o sa é refente ao SQLAlchemy

def upgrade():
    op.create_table('posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
