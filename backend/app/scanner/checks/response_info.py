class ResponseInfoChecker:
    """
    Collects general HTTP response information.

    This checker gathers passive metadata about the HTTP response.
    No security findings are generated in this module. The collected
    information is used to enrich the scan report.
    """

    def analyze(self, context: dict) -> dict:
        """
        Analyze the HTTP response.

        Args:
            context:
                {
                    "url": "...",
                    "response": requests.Response,
                    "elapsed_ms": float
                }

        Returns:
            Dictionary containing HTTP response information.
        """

        response = context["response"]

        elapsed_ms = context.get("elapsed_ms")

        headers = response.headers

        #
        # HTTP version
        #

        version_map = {
            9: "HTTP/0.9",
            10: "HTTP/1.0",
            11: "HTTP/1.1",
            20: "HTTP/2",
        }

        raw_version = getattr(
            response.raw,
            "version",
            None,
        )

        http_version = version_map.get(
            raw_version,
            f"HTTP/{raw_version}" if raw_version is not None else "Unknown",
        )

        #
        # Redirect information
        #

        redirect_count = len(response.history)

        #
        # Build response metadata
        #

        return {
            "http_version": http_version,
            "status_code": response.status_code,
            "response_time_ms": elapsed_ms,
            "final_url": response.url,
            "redirect_count": redirect_count,
            "content_type": headers.get("Content-Type"),
            "content_length": headers.get("Content-Length"),
            "content_encoding": headers.get("Content-Encoding"),
            "server": headers.get("Server"),
            "server_timing": headers.get("Server-Timing"),
            "findings": [],
        }