import requests


class SensitiveFileChecker:
    """
    Checks for exposed sensitive files.
    """

    SENSITIVE_PATHS = [
        "/.env",
        "/.git/config",
        "/backup.zip",
        "/backup.tar.gz",
        "/config.php.bak",
        "/database.sql",
    ]


    def analyze(self, context: dict) -> dict:
        """
        Scan common sensitive file locations.
        """

        base_url = context["url"]

        findings = []


        for path in self.SENSITIVE_PATHS:

            url = base_url.rstrip("/") + path

            try:

                response = requests.get(
                    url,
                    timeout=5,
                    allow_redirects=False,
                )


                exposed = (
                    response.status_code == 200
                    and len(response.text) > 0
                )


                findings.append(
                    {
                        "name": f"Sensitive File Exposure: {path}",
                        "severity": "High",
                        "status": (
                            "failed"
                            if exposed
                            else "passed"
                        ),
                        "description": (
                            "Sensitive file is publicly accessible."
                            if exposed
                            else "Sensitive file is not exposed."
                        ),
                        "value": (
                            url
                            if exposed
                            else None
                        ),
                    }
                )


            except Exception:

                findings.append(
                    {
                        "name": f"Sensitive File Exposure: {path}",
                        "severity": "High",
                        "status": "unknown",
                        "description": (
                            "Could not verify file exposure."
                        ),
                        "value": None,
                    }
                )


        return {
            "findings": findings
        }