"""empty message

Revision ID: 6f2942da1573
Revises: 
Create Date: 2022-07-15 00:53:27.020139

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6f2942da1573'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('masa', sa.String(length=200), nullable=True))
    op.add_column('events', sa.Column('nota', sa.String(length=2000), nullable=True))
    op.add_column('events', sa.Column('program', sa.String(length=200), nullable=True))
    op.add_column('events', sa.Column('tarikh', sa.Date(), nullable=True))
    op.add_column('events', sa.Column('tempat', sa.String(length=200), nullable=True))
    op.add_column('events', sa.Column('vvip', sa.String(length=200), nullable=True))
    op.drop_column('events', 'description')
    op.drop_column('events', 'name')
    op.drop_column('events', 'location')
    op.drop_column('events', 'startDate')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('startDate', sa.DATE(), nullable=True))
    op.add_column('events', sa.Column('location', mysql.VARCHAR(length=100), nullable=True))
    op.add_column('events', sa.Column('name', mysql.VARCHAR(length=100), nullable=True))
    op.add_column('events', sa.Column('description', mysql.VARCHAR(length=2000), nullable=True))
    op.drop_column('events', 'vvip')
    op.drop_column('events', 'tempat')
    op.drop_column('events', 'tarikh')
    op.drop_column('events', 'program')
    op.drop_column('events', 'nota')
    op.drop_column('events', 'masa')
    # ### end Alembic commands ###