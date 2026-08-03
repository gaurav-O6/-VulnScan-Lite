from datetime import datetime

from sqlalchemy import JSON

from app.extensions import db


class Scan(db.Model):
    """
    Stores metadata and the complete vulnerability scan report.
    """

    __tablename__ = "scans"


    id = db.Column(
        db.Integer,
        primary_key=True,
    )


    target_url = db.Column(
        db.String(500),
        nullable=False,
    )


    status = db.Column(
        db.String(20),
        nullable=False,
        default="queued",
    )


    progress = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )


    current_stage = db.Column(
        db.String(100),
        nullable=False,
        default="Queued",
    )


    score = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )


    grade = db.Column(
        db.String(5),
        nullable=False,
        default="F",
    )


    report_json = db.Column(
        JSON,
        nullable=True,
    )


    started_at = db.Column(
        db.DateTime,
        nullable=True,
    )


    completed_at = db.Column(
        db.DateTime,
        nullable=True,
    )


    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )


    def __repr__(self):
        return f"<Scan {self.id} - {self.target_url}>"