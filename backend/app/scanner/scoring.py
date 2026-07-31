class ScoringEngine:
    """
    Calculates security score from scan findings.
    """

    MAX_SCORE = 100

    SEVERITY_DEDUCTION = {
        "High": 10,
        "Medium": 5,
        "Low": 2,
    }

    def calculate(self, findings: list) -> dict:
        """
        Calculate security score.

        Args:
            findings:
                List of security findings.

        Returns:
            Score report.
        """

        score = self.MAX_SCORE

        summary = {
            "High": 0,
            "Medium": 0,
            "Low": 0,
        }

        failed_checks = []

        for finding in findings:

            if finding.get("status") != "failed":
                continue

            severity = finding.get(
                "severity",
                "Low"
            )

            deduction = self.SEVERITY_DEDUCTION.get(
                severity,
                0
            )

            score -= deduction

            summary[severity] += 1

            failed_checks.append(finding)

        score = max(score, 0)

        return {
            "score": score,
            "grade": self._grade(score),
            "summary": summary,
            "failed_checks": failed_checks,
        }

    def _grade(self, score: int) -> str:
        """
        Convert score to letter grade.
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