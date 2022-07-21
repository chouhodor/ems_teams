"""empty message

Revision ID: b41804420367
Revises: e2c809b97ee3
Create Date: 2022-07-21 11:42:33.061466

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b41804420367'
down_revision = 'e2c809b97ee3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('logs', sa.Column('tarikhmasa_log', sa.DateTime(), nullable=True))
    op.drop_column('logs', 'masa_log')
    op.drop_column('logs', 'tarikh_log')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('logs', sa.Column('tarikh_log', sa.DATE(), nullable=True))
    op.add_column('logs', sa.Column('masa_log', mysql.VARCHAR(length=200), nullable=True))
    op.drop_column('logs', 'tarikhmasa_log')
    # ### end Alembic commands ###
