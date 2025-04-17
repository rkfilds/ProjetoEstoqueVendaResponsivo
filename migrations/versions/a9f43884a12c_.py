"""empty message

Revision ID: a9f43884a12c
Revises: 
Create Date: 2025-04-15 23:09:04.468368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9f43884a12c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auditoria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario', sa.String(length=50), nullable=True),
    sa.Column('acao', sa.String(length=100), nullable=True),
    sa.Column('data_acao', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('produto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('marca', sa.String(length=50), nullable=True),
    sa.Column('classificacao', sa.String(length=50), nullable=True),
    sa.Column('modelo', sa.String(length=50), nullable=True),
    sa.Column('cor', sa.String(length=20), nullable=True),
    sa.Column('tamanho', sa.String(length=10), nullable=True),
    sa.Column('valor', sa.Integer(), nullable=True),
    sa.Column('data_entrada', sa.DateTime(), nullable=True),
    sa.Column('imagem', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venda',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('produto_id', sa.Integer(), nullable=True),
    sa.Column('quantidade', sa.Integer(), nullable=True),
    sa.Column('valor', sa.Integer(), nullable=True),
    sa.Column('data', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['produto_id'], ['produto.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venda')
    op.drop_table('produto')
    op.drop_table('auditoria')
    # ### end Alembic commands ###
