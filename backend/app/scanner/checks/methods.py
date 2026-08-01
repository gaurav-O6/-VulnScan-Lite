class HTTPMethodChecker:
    """
    Checks for potentially dangerous HTTP methods.
    """

    DANGEROUS_METHODS = {
        "TRACE": {
            "severity": "Medium",
            "description": (
                "TRACE method can expose request information "
                "and may enable Cross-Site Tracing attacks."
            ),
        },
        "PUT": {
            "severity": "Medium",
            "description": (
                "PUT method may allow unauthorized file "
                "or resource modification."
            ),
        },
        "DELETE": {
            "severity": "Medium",
            "description": (
                "DELETE method may allow unauthorized "
                "resource deletion."
            ),
        },
    }

    def analyze(self, context: dict) -> dict:
        """
        Analyze allowed HTTP methods.

        Note:
        This performs passive analysis using
        response headers where possible.
        """

        response = context["response"]

        findings = []

        allow_header = response.headers.get("Allow")

        if not allow_header:
            return {
                "findings": [
                    {
                        "name": "HTTP Method Exposure",
                        "status": "passed",
                        "severity": "Low",
                        "value": None,
                        "description": (
                            "No exposed HTTP methods detected."
                        ),
                    }
                ]
            }

        allowed_methods = [
            method.strip().upper()
            for method in allow_header.split(",")
        ]

        for method, metadata in self.DANGEROUS_METHODS.items():

            if method in allowed_methods:

                findings.append(
                    {
                        "name": f"{method} Method Enabled",
                        "status": "failed",
                        "severity": metadata["severity"],
                        "value": method,
                        "description": metadata["description"],
                    }
                )

            else:

                findings.append(
                    {
                        "name": f"{method} Method Enabled",
                        "status": "passed",
                        "severity": metadata["severity"],
                        "value": None,
                        "description": (
                            f"{method} method is not exposed."
                        ),
                    }
                )

        return {
            "findings": findings
        }