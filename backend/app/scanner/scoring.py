from app.scanner.finding import normalize_finding, normalize_severity


class ScoringEngine:
    """
    Calculates security score from standardized findings.
    """

    MAX_SCORE = 100

    SEVERITY_DEDUCTION = {
        "Critical": 20,
        "High": 10,
        "Medium": 5,
        "Low": 2,
        "Informational": 0,
    }

    def calculate(
        self,
        findings: list,
    ) -> dict:
        """
        Calculate security score.

        Accepts both:
        - old checker dictionaries
        - normalized findings
        """

        normalized_findings = []

        #
        # Normalize all findings first
        #

        for index, finding in enumerate(findings, start=1):

            if not isinstance(finding, dict):
                continue

            if "category" not in finding:

                finding = normalize_finding(
                    finding,
                    category="unknown",
                    finding_id=f"F-{index:04d}",
                )

            finding["severity"] = normalize_severity(
                finding.get(
                    "severity",
                    "Low",
                )
            )

            normalized_findings.append(
                finding
            )

        #
        # Remove duplicate findings.
        #
        # Duplicate definition:
        # Category + Name + Status
        #

        unique_findings = []
        seen = set()

        for finding in normalized_findings:

            key = (
                finding.get("category"),
                finding.get("name"),
                finding.get("status"),
            )

            if key in seen:
                continue

            seen.add(key)
            unique_findings.append(finding)

        score = self.MAX_SCORE

        summary = {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0,
            "Informational": 0,
        }

        passed_checks = []

        failed_checks = []

        statistics = {
            "total_checks": len(unique_findings),
            "passed_checks": 0,
            "failed_checks": 0,
            "unknown_checks": 0,
        }

        for finding in unique_findings:

            status = finding.get(
                "status",
                "unknown",
            )

            severity = finding.get(
                "severity",
                "Low",
            )

            if status == "passed":

                statistics["passed_checks"] += 1

                passed_checks.append(
                    finding
                )

                continue

            if status == "unknown":

                statistics["unknown_checks"] += 1

                continue

            if status != "failed":
                continue

            statistics["failed_checks"] += 1

            deduction = self.SEVERITY_DEDUCTION.get(
                severity,
                0,
            )

            score -= deduction

            if severity in summary:
                summary[severity] += 1

            failed_checks.append(
                finding
            )

        score = max(
            score,
            0,
        )

        return {
            "score": score,
            "grade": self._grade(score),
            "summary": summary,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "statistics": statistics,
        }

    def _grade(
        self,
        score: int,
    ) -> str:
        """
        Convert numeric score into grade.
        """

        if score >= 90:
            return "A"

        if score >= 80:
            return "B"

        if score >= 70:
            return "C"

        if score >= 60:
            return "D"

        return "F"