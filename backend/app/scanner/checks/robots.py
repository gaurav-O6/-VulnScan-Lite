from app.scanner.http_client import HTTPClient


class RobotsChecker:
    """
    Checks robots.txt for sensitive paths.
    """


    SUSPICIOUS_WORDS = [
        "admin",
        "backup",
        "database",
        "private",
        "config",
        "secret",
    ]


    def analyze(self, context: dict) -> dict:

        url = (
            context["url"].rstrip("/")
            + "/robots.txt"
        )


        http_client: HTTPClient = context["http_client"]

        findings = []


        try:

            result = http_client.get(url)


            if not result["success"]:

                findings.append(
                    {
                        "name": "Robots.txt Check",
                        "severity": "Low",
                        "status": "unknown",
                        "description": (
                            "Unable to check robots.txt."
                        ),
                        "value": None,
                    }
                )

                return {
                    "findings": findings
                }


            response = result["response"]


            if response.status_code != 200:

                return {
                    "findings": [
                        {
                            "name": "Robots.txt",
                            "severity": "Informational",
                            "status": "passed",
                            "description": (
                                "robots.txt not found."
                            ),
                            "value": None,
                        }
                    ]
                }


            lines = response.text.lower()


            exposed = []

            for word in self.SUSPICIOUS_WORDS:

                if word in lines:

                    exposed.append(word)


            findings.append(
                {
                    "name": "Robots.txt Sensitive Paths",
                    "severity": "Low",
                    "status": (
                        "failed"
                        if exposed
                        else "passed"
                    ),
                    "description": (
                        "robots.txt reveals potentially sensitive paths."
                        if exposed
                        else "No sensitive paths detected."
                    ),
                    "value": exposed or None,
                }
            )


        except Exception:

            findings.append(
                {
                    "name": "Robots.txt Check",
                    "severity": "Low",
                    "status": "unknown",
                    "description": (
                        "Unable to check robots.txt."
                    ),
                    "value": None,
                }
            )


        return {
            "findings": findings
        }