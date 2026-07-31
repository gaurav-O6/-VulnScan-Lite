from app.scanner.http_client import HTTPClient
from app.scanner.validator import URLValidator
from app.scanner.checks.headers import HeaderChecker


class Scanner:
    """
    Coordinates the scanning workflow.

    The Scanner orchestrates the different scanning components
    but does not perform the individual security checks itself.
    """

    def __init__(self):
        self.validator = URLValidator()
        self.http_client = HTTPClient()
        self.header_checker = HeaderChecker()

    def scan(self, url: str) -> dict:
        """
        Execute a vulnerability scan.

        Workflow:
        1. Validate the URL.
        2. Fetch the target.
        3. Build a scan context.
        4. Run security checks.
        5. Return the collected results.
        """

        validation = self.validator.validate(url)

        if not validation["valid"]:
            return {
                "success": False,
                "target": None,
                "status_code": None,
                "headers": None,
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
                "error": result["error"],
            }

        response = result["response"]

        context = {
            "url": target,
            "response": response,
        }

        header_results = self.header_checker.analyze(context)

        return {
            "success": True,
            "target": response.url,
            "status_code": response.status_code,
            "headers": header_results,
            "error": None,
        }

    def close(self):
        """
        Release resources held by the scanner.
        """
        self.http_client.close()