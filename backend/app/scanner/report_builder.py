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

            "target": target,

            "security_score": score,


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