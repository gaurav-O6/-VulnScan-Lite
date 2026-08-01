import requests


class SecurityTxtChecker:
    """
    Checks security.txt implementation.
    """


    def analyze(self, context: dict) -> dict:

        url = (
            context["url"].rstrip("/")
            + "/.well-known/security.txt"
        )


        try:

            response = requests.get(
                url,
                timeout=5,
            )


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
                        "value": url if exists else None,
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