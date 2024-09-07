"""empty message

Revision ID: be286a57d999
Revises: 5de8dd65b29f
Create Date: 2024-08-28 12:12:54.942574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be286a57d999'
down_revision = '5de8dd65b29f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.String(length=255), nullable=False))
        batch_op.drop_column('save_path')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('save_path', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
        batch_op.drop_column('image_url')

    # ### end Alembic commands ###