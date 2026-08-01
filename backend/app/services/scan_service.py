from datetime import datetime

from app.extensions import db
from app.models import Scan
from app.scanner.scanner import Scanner


class ScanService:
    """
    Service responsible for orchestrating vulnerability scans.
    """

    def __init__(self):
        self.scanner = Scanner()

    def run_scan(self, url: str) -> Scan:
        """
        Execute a vulnerability scan and persist the results.
        """

        scan = Scan(
            target_url=url,
            status="running",
            started_at=datetime.utcnow(),
        )

        db.session.add(scan)
        db.session.commit()

        try:
            result = self.scanner.scan(url)

            if not result["success"]:

                scan.status = "failed"
                scan.completed_at = datetime.utcnow()

                db.session.commit()

                return scan

            report = result["report"]
            security_score = report["security_score"]

            scan.status = "completed"
            scan.score = security_score["score"]
            scan.grade = security_score["grade"]

            #
            # Store the complete scan report.
            #
            scan.report_json = report

            scan.completed_at = datetime.utcnow()

            db.session.commit()

            return scan

        finally:
            self.scanner.close()

    def get_scan(self, scan_id: int) -> Scan | None:
        """
        Retrieve a scan by its ID.
        """

        return db.session.get(
            Scan,
            scan_id,
        )

    def get_all_scans(self) -> list[Scan]:
        """
        Retrieve all scans ordered by newest first.
        """

        return (
            Scan.query.order_by(
                Scan.created_at.desc()
            ).all()
        )