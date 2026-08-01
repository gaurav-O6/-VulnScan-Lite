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
            ssl_report = report["ssl"]
            technology = report["technology"]
            header_report = report["security_headers"]

            scan.status = "completed"

            scan.score = security_score["score"]
            scan.grade = security_score["grade"]

            scan.ssl_valid = ssl_report["valid"]
            scan.ssl_expiry = ssl_report["expires_on"]

            if technology["cms"]:
                scan.cms_name = technology["cms"][0]["name"]
            else:
                scan.cms_name = None

            scan.cms_version = None

            scan.headers_json = header_report
            scan.findings_json = security_score["failed_checks"]
            scan.remediation_json = None

            scan.completed_at = datetime.utcnow()

            db.session.commit()

            return scan

        finally:
            self.scanner.close()

    def get_scan(self, scan_id: int) -> Scan | None:
        """
        Retrieve a scan by its ID.

        Args:
            scan_id:
                Scan identifier.

        Returns:
            Scan instance if found, otherwise None.
        """

        return db.session.get(
            Scan,
            scan_id,
        )