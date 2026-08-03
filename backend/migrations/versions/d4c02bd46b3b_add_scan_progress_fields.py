"""add scan progress fields"""

from alembic import op
import sqlalchemy as sa


revision = "d4c02bd46b3b"
down_revision = "21c4edd80579"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("scans") as batch_op:

        batch_op.add_column(
            sa.Column(
                "progress",
                sa.Integer(),
                nullable=True,
            )
        )

        batch_op.add_column(
            sa.Column(
                "current_stage",
                sa.String(length=100),
                nullable=True,
            )
        )


    op.execute(
        """
        UPDATE scans
        SET progress = 0,
            current_stage = 'Queued'
        WHERE progress IS NULL
        """
    )


    with op.batch_alter_table("scans") as batch_op:

        batch_op.alter_column(
            "progress",
            nullable=False
        )

        batch_op.alter_column(
            "current_stage",
            nullable=False
        )



def downgrade():

    with op.batch_alter_table("scans") as batch_op:

        batch_op.drop_column(
            "current_stage"
        )

        batch_op.drop_column(
            "progress"
        )