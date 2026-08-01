class ExposureChecker:
    """
    Detects information disclosure through HTTP response headers.
    """

    def analyze(self, context: dict) -> dict:
        """
        Analyze response headers for
        unnecessary technology disclosure.
        """

        response = context["response"]

        findings = []

        server = response.headers.get("Server")

        if server:
            findings.append(
                {
                    "name": "Server Header Disclosure",
                    "status": "failed",
                    "severity": "Low",
                    "value": server,
                    "description": (
                        "Server header reveals "
                        "backend technology information."
                    ),
                }
            )
        else:
            findings.append(
                {
                    "name": "Server Header Disclosure",
                    "status": "passed",
                    "severity": "Low",
                    "value": None,
                    "description": (
                        "Server header information is hidden."
                    ),
                }
            )

        powered_by = response.headers.get(
            "X-Powered-By"
        )

        if powered_by:
            findings.append(
                {
                    "name": "X-Powered-By Disclosure",
                    "status": "failed",
                    "severity": "Low",
                    "value": powered_by,
                    "description": (
                        "X-Powered-By reveals "
                        "application technology."
                    ),
                }
            )
        else:
            findings.append(
                {
                    "name": "X-Powered-By Disclosure",
                    "status": "passed",
                    "severity": "Low",
                    "value": None,
                    "description": (
                        "Application technology header is hidden."
                    ),
                }
            )

        return {
            "findings": findings
        }