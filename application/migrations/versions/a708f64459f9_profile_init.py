"""Profile init

Revision ID: a708f64459f9
Revises: 
Create Date: 2024-06-21 19:31:44.020693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a708f64459f9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('displayName', sa.String(length=255), nullable=False),
    sa.Column('telegram', sa.Integer(), nullable=False),
    sa.Column('role', sa.Enum('user', 'moderator', 'admin', name='roleenum'), nullable=False),
    sa.Column('description', sa.String(length=600), nullable=False),
    sa.Column('visible', sa.Boolean(), nullable=False),
    sa.Column('avatar', sa.String(length=2048), nullable=True),
    sa.Column('city', sa.String(length=128), nullable=False),
    sa.Column('country', sa.String(length=128), nullable=False),
    sa.Column('personality', sa.String(length=4), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profile')
    # ### end Alembic commands ###
