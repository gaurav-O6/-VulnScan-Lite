class ScoringEngine:
    """
    Calculates security score from standardized findings.
    """

    MAX_SCORE = 100

    SEVERITY_DEDUCTION = {
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


        score = self.MAX_SCORE


        summary = {
            "High": 0,
            "Medium": 0,
            "Low": 0,
            "Informational": 0,
        }


        failed_checks = []


        for index, finding in enumerate(findings, start=1):

            if not isinstance(finding, dict):
                continue


            if "category" not in finding:

                from app.scanner.finding import normalize_finding

                finding = normalize_finding(
                    finding,
                    category="unknown",
                    finding_id=f"F-{index:04d}",
                )


            if finding.get("status") != "failed":
                continue


            severity = finding.get(
                "severity",
                "Low",
            )


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
            "failed_checks": failed_checks,
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