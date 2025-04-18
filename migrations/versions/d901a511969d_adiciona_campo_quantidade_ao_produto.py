"""Adiciona campo quantidade ao produto

Revision ID: d901a511969d
Revises: a9f43884a12c
Create Date: 2025-04-16 02:27:58.066003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd901a511969d'
down_revision = 'a9f43884a12c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantidade', sa.Integer(), nullable=True))
        batch_op.drop_column('classificacao')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('classificacao', sa.VARCHAR(length=50), nullable=True))
        batch_op.drop_column('quantidade')

    # ### end Alembic commands ###
