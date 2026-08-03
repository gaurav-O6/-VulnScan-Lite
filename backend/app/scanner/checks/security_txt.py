from app.scanner.http_client import HTTPClient


class SecurityTxtChecker:
    """
    Checks security.txt implementation.
    """


    def analyze(self, context: dict) -> dict:

        url = (
            context["url"].rstrip("/")
            + "/.well-known/security.txt"
        )


        http_client: HTTPClient = context["http_client"]


        try:

            result = http_client.get(url)


            if not result["success"]:

                return {
                    "findings": [
                        {
                            "name": "Security.txt",
                            "severity": "Informational",
                            "status": "unknown",
                            "description": (
                                "Unable to check security.txt."
                            ),
                            "value": None,
                        }
                    ]
                }


            response = result["response"]


            exists = response.status_code == 200


            return {
                "findings": [
                    {
                        "name": "Security.txt",
                        "severity": "Informational",
                        "status": (
                            "passed"
                            if exists
                            else "failed"
                        ),
                        "description": (
                            "security.txt is available."
                            if exists
                            else "security.txt file missing."
                        ),
                        "value": (
                            url
                            if exists
                            else None
                        ),
                    }
                ]
            }


        except Exception:

            return {
                "findings": [
                    {
                        "name": "Security.txt",
                        "severity": "Informational",
                        "status": "unknown",
                        "description": (
                            "Unable to check security.txt."
                        ),
                        "value": None,
                    }
                ]
            }