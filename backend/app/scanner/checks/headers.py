"""
HTTP Security Header Analysis

This module performs passive analysis of HTTP response headers.
It does not make network requests itself. Instead, it receives
the scan context from the Scanner and inspects the HTTP response.
"""

from requests import Response


SECURITY_HEADERS = {
    "Content-Security-Policy": {
        "severity": "High",
        "description": "Protects against Cross-Site Scripting (XSS).",
    },
    "Strict-Transport-Security": {
        "severity": "High",
        "description": "Forces browsers to use HTTPS.",
    },
    "X-Frame-Options": {
        "severity": "Medium",
        "description": "Prevents clickjacking attacks.",
    },
    "X-Content-Type-Options": {
        "severity": "Medium",
        "description": "Prevents MIME type sniffing.",
    },
    "Referrer-Policy": {
        "severity": "Low",
        "description": "Controls how much referrer information is shared.",
    },
    "Permissions-Policy": {
        "severity": "Low",
        "description": "Restricts access to browser features.",
    },
}


class HeaderChecker:
    """
    Performs passive HTTP security header analysis.

    This checker does not perform HTTP requests.
    It analyzes an already-fetched Response object.
    """

    def analyze(self, context: dict) -> dict:
        """
        Analyze HTTP security headers.

        Args:
            context:
                {
                    "url": "...",
                    "response": requests.Response
                }

        Returns:
            {
                "findings": [...]
            }
        """

        response: Response = context["response"]

        findings = []

        for header_name, metadata in SECURITY_HEADERS.items():

            if header_name in response.headers:

                findings.append(
                    {
                        "name": header_name,
                        "status": "passed",
                        "severity": metadata["severity"],
                        "value": response.headers.get(header_name),
                        "description": metadata["description"],
                    }
                )

            else:

                findings.append(
                    {
                        "name": header_name,
                        "status": "failed",
                        "severity": metadata["severity"],
                        "value": None,
                        "description": metadata["description"],
                    }
                )

        return {
            "findings": findings
        }