from app.scanner.http_client import HTTPClient
from app.scanner.validator import URLValidator

from app.scanner.checks.headers import HeaderChecker
from app.scanner.checks.ssl_check import SSLChecker
from app.scanner.checks.cms import CMSDetector
from app.scanner.checks.cookies import CookieChecker
from app.scanner.checks.exposure import ExposureChecker
from app.scanner.checks.methods import HTTPMethodChecker

from app.scanner.scoring import ScoringEngine
from app.scanner.report_builder import ReportBuilder


class Scanner:
    """
    Coordinates the vulnerability scanning workflow.

    Scanner acts as the orchestrator.
    Individual security checks are handled
    by separate modules.
    """

    def __init__(self):

        self.validator = URLValidator()

        self.http_client = HTTPClient()

        self.header_checker = HeaderChecker()

        self.ssl_checker = SSLChecker()

        self.cms_detector = CMSDetector()

        self.cookie_checker = CookieChecker()

        self.exposure_checker = ExposureChecker()

        self.http_method_checker = HTTPMethodChecker()

        self.scoring_engine = ScoringEngine()

        self.report_builder = ReportBuilder()


    def scan(self, url: str) -> dict:
        """
        Execute complete vulnerability scan.

        Workflow:

        1. Validate URL
        2. Fetch target
        3. Create scan context
        4. Run security checks
        5. Calculate score
        6. Build final report
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


        response_result = self.http_client.get(target)


        if not response_result["success"]:

            return {
                "success": False,
                "target": target,
                "status_code": None,
                "report": None,
                "error": response_result["error"],
            }


        response = response_result["response"]


        context = {
            "url": target,
            "response": response,
        }



        #
        # Security checks
        #

        header_results = self.header_checker.analyze(
            context
        )


        ssl_results = self.ssl_checker.analyze(
            context
        )


        technology_results = self.cms_detector.analyze(
            context
        )


        cookie_results = self.cookie_checker.analyze(
            context
        )


        exposure_results = self.exposure_checker.analyze(
            context
        )


        http_method_results = self.http_method_checker.analyze(
            context
        )



        #
        # Combine findings
        #

        findings = []


        findings.extend(
            header_results.get(
                "findings",
                []
            )
        )


        findings.extend(
            cookie_results.get(
                "findings",
                []
            )
        )


        findings.extend(
            exposure_results.get(
                "findings",
                []
            )
        )


        findings.extend(
            http_method_results.get(
                "findings",
                []
            )
        )



        #
        # Calculate security score
        #

        score_results = self.scoring_engine.calculate(
            findings
        )



        #
        # Generate final report
        #

        report = self.report_builder.build(
            target=response.url,
            headers=header_results,
            ssl=ssl_results,
            technology=technology_results,
            cookies=cookie_results,
            exposure=exposure_results,
            http_methods=http_method_results,
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
        Release scanner resources.
        """

        self.http_client.close()