"""coluna content adicionadana tabela posts

Revision ID: d7b3f10aaebd
Revises: 7f15802aa234
Create Date: 2021-12-16 18:58:57.882401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7b3f10aaebd'
down_revision = '7f15802aa234'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
