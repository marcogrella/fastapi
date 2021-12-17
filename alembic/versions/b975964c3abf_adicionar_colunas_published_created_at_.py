"""adicionar colunas published, created-at na tabela posts

Revision ID: b975964c3abf
Revises: db97703ab012
Create Date: 2021-12-17 11:26:35.480071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b975964c3abf'
down_revision = 'db97703ab012'
branch_labels = None
depends_on = None

# adicionar as demais colunas na tabela posts

def upgrade():
    op.add_column('posts', 
        sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                server_default=sa.text('now()'), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
