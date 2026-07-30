import requests


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
        "description": "Stops MIME-type sniffing.",
    },
    "Referrer-Policy": {
        "severity": "Low",
        "description": "Controls referrer information leakage.",
    },
    "Permissions-Policy": {
        "severity": "Low",
        "description": "Restricts browser feature access.",
    },
}


class HeaderChecker:
    """
    Performs passive HTTP header analysis.
    """

    def __init__(self, timeout=10):
        self.timeout = timeout

    def scan(self, url):
        """
        Scan HTTP response headers.
        """

        response = requests.get(
            url,
            timeout=self.timeout,
            allow_redirects=True,
            headers={
                "User-Agent": "VulnScanLite/1.0"
            },
        )

        headers = response.headers

        passed = []
        failed = []

        for header, info in SECURITY_HEADERS.items():

            if header in headers:

                passed.append(
                    {
                        "header": header,
                        "severity": info["severity"],
                        "value": headers.get(header),
                    }
                )

            else:

                failed.append(
                    {
                        "header": header,
                        "severity": info["severity"],
                        "description": info["description"],
                    }
                )

        server = headers.get("Server")

        return {
            "url": response.url,
            "status_code": response.status_code,
            "server": server,
            "passed": passed,
            "failed": failed,
        }