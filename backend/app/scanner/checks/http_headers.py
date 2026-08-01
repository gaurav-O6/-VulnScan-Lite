class HTTPHeaderAnalyzer:
    """
    Performs analysis of general HTTP response headers.

    This module focuses on operational HTTP headers rather than
    security headers such as CSP or HSTS.
    """

    HEADER_DESCRIPTIONS = {
        "Cache-Control": "Controls how responses are cached.",
        "ETag": "Provides a resource version identifier for cache validation.",
        "Age": "Indicates how long a response has been cached.",
        "Vary": "Specifies which request headers influence cached responses.",
        "Via": "Identifies intermediate proxies or gateways.",
        "Alt-Svc": "Advertises alternative HTTP services such as HTTP/3.",
        "Keep-Alive": "Provides connection persistence parameters.",
        "Connection": "Controls whether the network connection remains open.",
        "Transfer-Encoding": "Describes how the response body is transferred.",
    }

    def analyze(self, context: dict) -> dict:
        """
        Analyze non-security HTTP response headers.
        """

        response = context["response"]
        headers = response.headers

        results = {
            "headers": {},
            "findings": [],
        }

        for header_name, description in self.HEADER_DESCRIPTIONS.items():

            value = headers.get(header_name)

            results["headers"][header_name] = {
                "present": value is not None,
                "value": value,
                "description": description,
            }

            if value is None:
                continue

            finding = {
                "name": header_name,
                "status": "info",
                "severity": "Informational",
                "description": description,
                "value": value,
            }

            #
            # Header-specific observations
            #

            if header_name == "Cache-Control":

                if "no-store" in value.lower():
                    finding["note"] = (
                        "Sensitive content is instructed not to be stored by caches."
                    )

                elif "public" in value.lower():
                    finding["note"] = (
                        "Public caching is enabled."
                    )

            elif header_name == "ETag":

                finding["note"] = (
                    "Entity tags improve client-side cache validation."
                )

            elif header_name == "Age":

                finding["note"] = (
                    "Response appears to have been served from a cache."
                )

            elif header_name == "Via":

                finding["note"] = (
                    "Intermediate proxy or CDN detected."
                )

            elif header_name == "Alt-Svc":

                finding["note"] = (
                    "Alternative HTTP service advertised."
                )

            elif header_name == "Keep-Alive":

                finding["note"] = (
                    "Persistent HTTP connections are enabled."
                )

            elif header_name == "Connection":

                finding["note"] = (
                    f"Connection directive is '{value}'."
                )

            elif header_name == "Transfer-Encoding":

                finding["note"] = (
                    f"Transfer encoding is '{value}'."
                )

            elif header_name == "Vary":

                finding["note"] = (
                    "Caching varies depending on request headers."
                )

            results["findings"].append(finding)

        return results