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

                "summary": score.get(
                    "summary",
                    {},
                ),
            },


            "summary": self._build_summary(
                score
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


            # Backwards compatibility
            # Keep existing frontend/API consumers working

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
        score: dict,
    ) -> dict:
        """
        Build vulnerability summary.
        """

        severity_summary = score.get(
            "summary",
            {},
        )


        return {

            "total_findings": sum(
                severity_summary.values()
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
        Extract remediation recommendations.
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


        return list(
            dict.fromkeys(
                recommendations
            )
        )