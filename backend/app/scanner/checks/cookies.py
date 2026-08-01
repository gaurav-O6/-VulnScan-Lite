class CookieChecker:
    """
    Analyzes cookie security attributes.
    """

    def analyze(self, context: dict) -> dict:
        """
        Analyze cookies from HTTP response.

        Checks:
        - Secure flag
        - HttpOnly flag
        - SameSite attribute
        """

        response = context["response"]

        findings = []

        cookies = response.headers.get("Set-Cookie")

        if not cookies:
            return {
                "findings": [
                    {
                        "name": "Cookie Security",
                        "status": "passed",
                        "severity": "Low",
                        "description": "No cookies detected.",
                    }
                ]
            }

        cookie_lower = cookies.lower()

        if "httponly" not in cookie_lower:
            findings.append(
                {
                    "name": "Missing HttpOnly Cookie Flag",
                    "status": "failed",
                    "severity": "Medium",
                    "description": (
                        "Cookies without HttpOnly "
                        "may be accessible through JavaScript."
                    ),
                }
            )
        else:
            findings.append(
                {
                    "name": "HttpOnly Cookie Flag",
                    "status": "passed",
                    "severity": "Medium",
                    "description": "HttpOnly flag is configured.",
                }
            )

        if "secure" not in cookie_lower:
            findings.append(
                {
                    "name": "Missing Secure Cookie Flag",
                    "status": "failed",
                    "severity": "Medium",
                    "description": (
                        "Cookies without Secure flag "
                        "can be transmitted over HTTP."
                    ),
                }
            )
        else:
            findings.append(
                {
                    "name": "Secure Cookie Flag",
                    "status": "passed",
                    "severity": "Medium",
                    "description": "Secure flag is configured.",
                }
            )

        if "samesite" not in cookie_lower:
            findings.append(
                {
                    "name": "Missing SameSite Cookie Attribute",
                    "status": "failed",
                    "severity": "Low",
                    "description": (
                        "SameSite helps prevent CSRF attacks."
                    ),
                }
            )
        else:
            findings.append(
                {
                    "name": "SameSite Cookie Attribute",
                    "status": "passed",
                    "severity": "Low",
                    "description": "SameSite attribute is configured.",
                }
            )

        return {
            "findings": findings
        }