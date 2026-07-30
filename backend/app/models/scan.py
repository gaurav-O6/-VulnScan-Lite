from datetime import datetime

from sqlalchemy import JSON

from app.extensions import db


class Scan(db.Model):
    """
    Stores the result of a vulnerability scan.
    """

    __tablename__ = "scans"

    id = db.Column(db.Integer, primary_key=True)

    target_url = db.Column(db.String(500), nullable=False)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="queued",
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

    ssl_valid = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    ssl_expiry = db.Column(
        db.String(100),
        nullable=True,
    )

    cms_name = db.Column(
        db.String(100),
        nullable=True,
    )

    cms_version = db.Column(
        db.String(50),
        nullable=True,
    )

    headers_json = db.Column(
        JSON,
        nullable=True,
    )

    findings_json = db.Column(
        JSON,
        nullable=True,
    )

    remediation_json = db.Column(
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