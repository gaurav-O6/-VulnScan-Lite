class ReportBuilder:
    """
    Builds a standardized vulnerability scan report.
    """

    def build(
        self,
        target: str,
        headers: dict,
        ssl: dict,
        technology: dict,
        cookies: dict,
        exposure: dict,
        http_methods: dict,
        score: dict,
    ) -> dict:
        """
        Create final scan report.

        Args:
            target:
                Scanned URL.

            headers:
                HTTP security header analysis result.

            ssl:
                SSL inspection result.

            technology:
                CMS and technology detection result.

            cookies:
                Cookie security analysis result.

            exposure:
                Information disclosure analysis result.

            http_methods:
                HTTP method security analysis result.

            score:
                Security scoring result.

        Returns:
            Structured vulnerability scan report.
        """

        return {
            "target": target,
            "security_score": score,
            "security_headers": headers,
            "ssl": ssl,
            "technology": technology,
            "cookies": cookies,
            "exposure": exposure,
            "http_methods": http_methods,
        }