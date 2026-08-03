from datetime import datetime


class ReportBuilder:
    """
    Builds a standardized vulnerability scan report.
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
            # New Day 7 report sections
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

            "risk_overview": {
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
            },

            #
            # Existing summary retained
            #

            "summary": self._build_summary(
                severity_summary
            ),

            "recommendations": self._build_recommendations(
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

    def _build_recommendations(
        self,
        score: dict,
    ) -> list:
        """
        Extract unique remediation recommendations.
        """

        recommendations = []

        for finding in score.get(
            "failed_checks",
            [],
        ):

            recommendation = finding.get(
                "recommendation"
            )

            if recommendation:
                recommendations.append(
                    recommendation
                )

        #
        # Preserve insertion order while removing duplicates.
        #

        return list(
            dict.fromkeys(
                recommendations
            )
        )