"""Remove new_column from User

Revision ID: 48d19d7352ab
Revises: ca36a4a39732
Create Date: 2024-10-06 15:46:58.394833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '48d19d7352ab'
down_revision: Union[str, None] = 'ca36a4a39732'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
