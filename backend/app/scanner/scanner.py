from app.scanner.http_client import HTTPClient
from app.scanner.validator import URLValidator
from app.scanner.checks.headers import HeaderChecker
from app.scanner.checks.ssl_check import SSLChecker
from app.scanner.checks.cms import CMSDetector


class Scanner:
    """
    Coordinates the scanning workflow.

    The Scanner orchestrates different security checks
    but does not perform the checks itself.
    """

    def __init__(self):
        self.validator = URLValidator()
        self.http_client = HTTPClient()

        self.header_checker = HeaderChecker()
        self.ssl_checker = SSLChecker()
        self.cms_detector = CMSDetector()

    def scan(self, url: str) -> dict:
        """
        Execute a vulnerability scan.

        Workflow:
        1. Validate URL.
        2. Fetch target.
        3. Create scan context.
        4. Run security checks.
        5. Return combined results.
        """

        validation = self.validator.validate(url)

        if not validation["valid"]:
            return {
                "success": False,
                "target": None,
                "status_code": None,
                "headers": None,
                "ssl": None,
                "technology": None,
                "error": validation["error"],
            }

        target = validation["normalized_url"]

        result = self.http_client.get(target)

        if not result["success"]:
            return {
                "success": False,
                "target": target,
                "status_code": None,
                "headers": None,
                "ssl": None,
                "technology": None,
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

        return {
            "success": True,
            "target": response.url,
            "status_code": response.status_code,
            "headers": header_results,
            "ssl": ssl_results,
            "technology": technology_results,
            "error": None,
        }

    def close(self):
        """
        Release resources held by the scanner.
        """
        self.http_client.close()