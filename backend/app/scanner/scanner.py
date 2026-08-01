from app.scanner.http_client import HTTPClient
from app.scanner.validator import URLValidator
from app.scanner.checks.headers import HeaderChecker
from app.scanner.checks.ssl_check import SSLChecker
from app.scanner.checks.cms import CMSDetector
from app.scanner.scoring import ScoringEngine
from app.scanner.report_builder import ReportBuilder


class Scanner:
    """
    Coordinates the vulnerability scanning workflow.

    The Scanner orchestrates different security checks
    but does not perform the checks itself.
    """

    def __init__(self):
        self.validator = URLValidator()
        self.http_client = HTTPClient()

        self.header_checker = HeaderChecker()
        self.ssl_checker = SSLChecker()
        self.cms_detector = CMSDetector()

        self.scoring_engine = ScoringEngine()
        self.report_builder = ReportBuilder()

    def scan(self, url: str) -> dict:
        """
        Execute a vulnerability scan.

        Workflow:
        1. Validate URL.
        2. Fetch target.
        3. Run security checks.
        4. Calculate security score.
        5. Build final report.
        """

        validation = self.validator.validate(url)

        if not validation["valid"]:
            return {
                "success": False,
                "target": None,
                "status_code": None,
                "report": None,
                "error": validation["error"],
            }

        target = validation["normalized_url"]

        result = self.http_client.get(target)

        if not result["success"]:
            return {
                "success": False,
                "target": target,
                "status_code": None,
                "report": None,
                "error": result["error"],
            }

        response = result["response"]

        context = {
            "url": target,
            "response": response,
        }

        header_results = self.header_checker.analyze(context)
        ssl_results = self.ssl_checker.analyze(context)
        technology_results = self.cms_detector.analyze(context)

        score_results = self.scoring_engine.calculate(
            header_results["findings"]
        )

        report = self.report_builder.build(
            target=response.url,
            headers=header_results,
            ssl=ssl_results,
            technology=technology_results,
            score=score_results,
        )

        return {
            "success": True,
            "target": response.url,
            "status_code": response.status_code,
            "report": report,
            "error": None,
        }

    def close(self):
        """
        Release resources held by the scanner.
        """
        self.http_client.close()