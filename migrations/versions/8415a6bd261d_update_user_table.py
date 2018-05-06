"""update user table

Revision ID: 8415a6bd261d
Revises: 03553bbe81b1
Create Date: 2018-05-05 22:26:41.834763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8415a6bd261d'
down_revision = '03553bbe81b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    # ### end Alembic commands ###
