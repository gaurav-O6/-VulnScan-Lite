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
        score: dict,
    ) -> dict:
        """
        Create final scan report.

        Args:
            target:
                Scanned URL.

            headers:
                Header analysis result.

            ssl:
                SSL inspection result.

            technology:
                CMS and technology detection result.

            score:
                Security score result.

        Returns:
            Structured scan report.
        """

        return {
            "target": target,
            "security_score": score,
            "security_headers": headers,
            "ssl": ssl,
            "technology": technology,
        }