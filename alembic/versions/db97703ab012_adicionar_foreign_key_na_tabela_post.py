"""adicionar foreign-key na tabela post

Revision ID: db97703ab012
Revises: 7a98bf470d0b
Create Date: 2021-12-17 11:02:32.562402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db97703ab012'
down_revision = '7a98bf470d0b'
branch_labels = None
depends_on = None


def upgrade():
    # nessa linha cria-se somente a coluna
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    # aqui cria-se a referẽncia da fk com a tabela e coluna:
    # source_table="posts" tabela que irá receber a fk
    # referent_table="users" tabela de referência que fornece a fk
    # local_cols=['user_id'] coluna que irá receber a fk (criada acima)
    # remote_cols=['id'] coluna de referência da tabela que fornece a fk (no caso users)
    op.create_foreign_key('posts_users_fk', source_table="posts", 
        referent_table="users", local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
