"""Init

Revision ID: 2c3c4f33b7c1
Revises: 
Create Date: 2024-08-22 16:39:18.400634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c3c4f33b7c1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('displayName', sa.String(length=255), nullable=False),
    sa.Column('telegram', sa.BigInteger(), nullable=False),
    sa.Column('role', sa.Enum('user', 'admin', name='roleenum'), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=True),
    sa.Column('avatar', sa.String(length=2048), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lesson',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('tasks', sa.JSON(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('lesson_id', sa.UUID(), nullable=False),
    sa.Column('type', sa.Enum('translation', 'fill_in', 'multiple_choice', 'matching', 'rearrange', name='tasktypeenum'), nullable=False),
    sa.Column('question', sa.String(), nullable=False),
    sa.Column('answer', sa.String(), nullable=False),
    sa.Column('correct', sa.Boolean(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    op.drop_table('lesson')
    op.drop_table('profile')
    # ### end Alembic commands ###
