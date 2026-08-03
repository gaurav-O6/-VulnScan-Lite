from datetime import datetime


class ReportBuilder:
    """
    Builds a standardized vulnerability scan report.

    Responsible for report interpretation only.
    PDF/HTML generators should consume this output.
    """

    def build(
        self,
        target: str,
        response_info: dict,
        http_headers: dict,
        headers: dict,
        ssl: dict,
        technology: dict,
        cookies: dict,
        exposure: dict,
        http_methods: dict,
        files: dict,
        robots: dict,
        security_txt: dict,
        score: dict,
    ) -> dict:
        """
        Create final scan report.
        """

        statistics = score.get(
            "statistics",
            {},
        )

        severity_summary = score.get(
            "summary",
            {},
        )

        risk_overview = self._build_risk_overview(
            severity_summary
        )

        return {

            "metadata": {
                "scanner": "VulnScanLite",
                "version": "1.0",
                "generated_at": datetime.utcnow().isoformat(),
            },

            "target": {
                "url": target,
            },

            "security_score": {
                "score": score.get(
                    "score",
                    0,
                ),
                "grade": score.get(
                    "grade",
                    "F",
                ),
                "summary": severity_summary,
            },

            #
            # Day 7 summary retained
            #

            "scan_summary": {
                "total_checks": statistics.get(
                    "total_checks",
                    0,
                ),
                "passed_checks": statistics.get(
                    "passed_checks",
                    0,
                ),
                "failed_checks": statistics.get(
                    "failed_checks",
                    0,
                ),
                "unknown_checks": statistics.get(
                    "unknown_checks",
                    0,
                ),
            },

            #
            # Improved Day 8 risk overview
            #

            "risk_overview": risk_overview,

            #
            # New Day 8 reporting sections
            #

            "executive_summary": self._build_executive_summary(
                score,
                risk_overview,
            ),

            "success_rate": self._build_success_rate(
                statistics
            ),

            #
            # Existing summary retained
            #

            "summary": self._build_summary(
                severity_summary
            ),

            "recommendations": self._build_recommendations(
                score
            ),

            "recommendation_groups": self._build_recommendation_groups(
                score
            ),

            "technical_details": {

                "response_info": response_info,

                "http_headers": http_headers,

                "security_headers": headers,

                "ssl": ssl,

                "technology": technology,

                "cookies": cookies,

                "exposure": exposure,

                "http_methods": http_methods,

                "sensitive_files": files,

                "robots_txt": robots,

                "security_txt": security_txt,
            },

            #
            # Backwards compatibility
            #

            "response_info": response_info,

            "http_headers": http_headers,

            "security_headers": headers,

            "ssl": ssl,

            "technology": technology,

            "cookies": cookies,

            "exposure": exposure,

            "http_methods": http_methods,

            "sensitive_files": files,

            "robots_txt": robots,

            "security_txt": security_txt,
        }

    def _build_summary(
        self,
        severity_summary: dict,
    ) -> dict:
        """
        Build vulnerability summary.
        """

        return {

            "total_findings": sum(
                severity_summary.values()
            ),

            "critical": severity_summary.get(
                "Critical",
                0,
            ),

            "high": severity_summary.get(
                "High",
                0,
            ),

            "medium": severity_summary.get(
                "Medium",
                0,
            ),

            "low": severity_summary.get(
                "Low",
                0,
            ),

            "informational": severity_summary.get(
                "Informational",
                0,
            ),
        }

    def _build_risk_overview(
        self,
        severity_summary: dict,
    ) -> dict:
        """
        Build richer risk interpretation.
        """

        overview = {

            "critical": severity_summary.get(
                "Critical",
                0,
            ),

            "high": severity_summary.get(
                "High",
                0,
            ),

            "medium": severity_summary.get(
                "Medium",
                0,
            ),

            "low": severity_summary.get(
                "Low",
                0,
            ),

            "informational": severity_summary.get(
                "Informational",
                0,
            ),
        }

        highest = "None"

        severity_order = [
            "Critical",
            "High",
            "Medium",
            "Low",
            "Informational",
        ]

        for severity in severity_order:

            if severity_summary.get(
                severity,
                0,
            ) > 0:
                highest = severity
                break

        overview["highest_severity"] = highest

        if highest == "Critical":
            risk = "Critical"
            description = (
                "Critical security issues were detected "
                "and require immediate attention."
            )

        elif highest == "High":
            risk = "High"
            description = (
                "High severity issues were detected "
                "and should be remediated soon."
            )

        elif highest == "Medium":
            risk = "Medium"
            description = (
                "The target has moderate security weaknesses."
            )

        elif highest == "Low":
            risk = "Low"
            description = (
                "Only low impact security issues were detected."
            )

        else:
            risk = "Secure"
            description = (
                "No significant security issues were detected."
            )

        overview["overall_risk"] = risk
        overview["risk_description"] = description

        return overview

    def _build_success_rate(
        self,
        statistics: dict,
    ) -> dict:
        """
        Calculate successful security check percentage.
        """

        total = statistics.get(
            "total_checks",
            0,
        )

        passed = statistics.get(
            "passed_checks",
            0,
        )

        if total == 0:
            percentage = 0

        else:
            percentage = round(
                (passed / total) * 100,
                2,
            )

        return {

            "percentage": percentage,

            "passed_checks": passed,

            "total_checks": total,

        }

    def _build_executive_summary(
        self,
        score: dict,
        risk_overview: dict,
    ) -> dict:
        """
        Generate human readable scan summary.
        """

        security_score = score.get(
            "score",
            0,
        )

        grade = score.get(
            "grade",
            "F",
        )

        total_findings = sum(
            score.get(
                "summary",
                {},
            ).values()
        )

        risk = risk_overview.get(
            "overall_risk",
            "Unknown",
        )

        return {

            "headline": (
                f"{risk} security posture detected"
            ),

            "description": (
                f"The scan completed with a "
                f"security score of "
                f"{security_score}/100 "
                f"(Grade {grade}). "
                f"{total_findings} security findings "
                f"were identified."
            ),

            "priority": risk,

        }

    def _build_recommendation_groups(
        self,
        score: dict,
    ) -> dict:
        """
        Group recommendations by severity.
        """

        groups = {

            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
            "general": [],
        }

        seen = set()

        for finding in score.get(
            "failed_checks",
            [],
        ):

            recommendation = finding.get(
                "recommendation"
            )

            if not recommendation:
                continue

            if recommendation in seen:
                continue

            seen.add(
                recommendation
            )

            severity = finding.get(
                "severity",
                "Low",
            ).lower()

            if severity in groups:
                groups[severity].append(
                    recommendation
                )

            else:
                groups["general"].append(
                    recommendation
                )

        return groups

    def _build_recommendations(
        self,
        score: dict,
    ) -> list:
        """
        Extract unique prioritized remediation recommendations.
        """

        priority_order = {
            "Critical": 0,
            "High": 1,
            "Medium": 2,
            "Low": 3,
            "Informational": 4,
        }

        recommendations = []

        findings = score.get(
            "failed_checks",
            [],
        )

        sorted_findings = sorted(
            findings,
            key=lambda item: priority_order.get(
                item.get(
                    "severity",
                    "Low",
                ),
                5,
            ),
        )

        for finding in sorted_findings:

            recommendation = finding.get(
                "recommendation"
            )

            if recommendation:
                recommendations.append(
                    recommendation
                )

        return list(
            dict.fromkeys(
                recommendations
            )
        )