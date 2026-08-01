from app.scanner.http_client import HTTPClient
from app.scanner.validator import URLValidator

from app.scanner.checks.headers import HeaderChecker
from app.scanner.checks.http_headers import HTTPHeaderAnalyzer
from app.scanner.checks.ssl_check import SSLChecker
from app.scanner.checks.cms import CMSDetector
from app.scanner.checks.cookies import CookieChecker
from app.scanner.checks.exposure import ExposureChecker
from app.scanner.checks.methods import HTTPMethodChecker
from app.scanner.checks.response_info import ResponseInfoChecker

from app.scanner.checks.files import SensitiveFileChecker
from app.scanner.checks.robots import RobotsChecker
from app.scanner.checks.security_txt import SecurityTxtChecker

from app.scanner.finding import normalize_finding

from app.scanner.scoring import ScoringEngine
from app.scanner.report_builder import ReportBuilder


class Scanner:
    """
    Coordinates complete vulnerability scanning workflow.
    """

    def __init__(self):

        self.validator = URLValidator()

        self.http_client = HTTPClient()

        self.header_checker = HeaderChecker()

        self.http_header_analyzer = HTTPHeaderAnalyzer()

        self.ssl_checker = SSLChecker()

        self.cms_detector = CMSDetector()

        self.cookie_checker = CookieChecker()

        self.exposure_checker = ExposureChecker()

        self.http_method_checker = HTTPMethodChecker()

        self.response_info_checker = ResponseInfoChecker()

        self.file_checker = SensitiveFileChecker()

        self.robots_checker = RobotsChecker()

        self.security_txt_checker = SecurityTxtChecker()

        self.scoring_engine = ScoringEngine()

        self.report_builder = ReportBuilder()


    def scan(self, url: str) -> dict:
        """
        Execute complete vulnerability scan.
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
            "elapsed_ms": response_result["elapsed_ms"],
        }


        response_info_results = self.response_info_checker.analyze(
            context
        )


        http_header_results = self.http_header_analyzer.analyze(
            context
        )


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


        file_results = self.file_checker.analyze(
            context
        )


        robots_results = self.robots_checker.analyze(
            context
        )


        security_txt_results = self.security_txt_checker.analyze(
            context
        )


        raw_findings = []


        raw_findings.extend(
            header_results.get(
                "findings",
                []
            )
        )


        raw_findings.extend(
            cookie_results.get(
                "findings",
                []
            )
        )


        raw_findings.extend(
            exposure_results.get(
                "findings",
                []
            )
        )


        raw_findings.extend(
            http_method_results.get(
                "findings",
                []
            )
        )


        raw_findings.extend(
            file_results.get(
                "findings",
                []
            )
        )


        raw_findings.extend(
            robots_results.get(
                "findings",
                []
            )
        )


        raw_findings.extend(
            security_txt_results.get(
                "findings",
                []
            )
        )


        findings = []


        for index, finding in enumerate(
            raw_findings,
            start=1
        ):

            findings.append(
                normalize_finding(
                    finding,
                    category="security",
                    finding_id=f"FIND-{index:03}",
                )
            )


        score_results = self.scoring_engine.calculate(
            findings
        )


        report = self.report_builder.build(
            target=response.url,
            response_info=response_info_results,
            http_headers=http_header_results,
            headers=header_results,
            ssl=ssl_results,
            technology=technology_results,
            cookies=cookie_results,
            exposure=exposure_results,
            http_methods=http_method_results,
            files=file_results,
            robots=robots_results,
            security_txt=security_txt_results,
            score=score_results,
        )


        report["findings"] = findings


        return {
            "success": True,
            "target": response.url,
            "status_code": response.status_code,
            "report": report,
            "error": None,
        }


    def close(self):

        self.http_client.close()