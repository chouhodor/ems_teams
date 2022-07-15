"""empty message

Revision ID: e2c809b97ee3
Revises: 6f2942da1573
Create Date: 2022-07-15 12:20:40.497011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2c809b97ee3'
down_revision = '6f2942da1573'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('program_log', sa.String(length=200), nullable=True),
    sa.Column('tarikh_log', sa.Date(), nullable=True),
    sa.Column('masa_log', sa.String(length=200), nullable=True),
    sa.Column('event_change', sa.String(length=200), nullable=True),
    sa.Column('changer', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('events', sa.Column('status', sa.String(length=200), nullable=True))
    op.add_column('user', sa.Column('role', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    op.drop_column('events', 'status')
    op.drop_table('logs')
    # ### end Alembic commands ###
