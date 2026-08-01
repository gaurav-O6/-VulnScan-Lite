from time import perf_counter
from typing import Optional

import requests
from requests import Response
from requests.exceptions import RequestException


class HTTPClient:
    """
    Reusable HTTP client for VulnScan Lite.

    All outbound HTTP requests should go through this class.
    """

    DEFAULT_USER_AGENT = (
        "VulnScanLite/1.0 (+https://github.com/yourusername/VulnScanLite)"
    )

    def __init__(
        self,
        timeout: int = 10,
        verify_ssl: bool = True,
        allow_redirects: bool = True,
    ):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.allow_redirects = allow_redirects

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": self.DEFAULT_USER_AGENT,
            }
        )

    def get(self, url: str) -> dict:
        """
        Send an HTTP GET request.

        Returns:
            {
                "success": bool,
                "response": Response | None,
                "elapsed_ms": float | None,
                "error": str | None
            }
        """

        start_time = perf_counter()

        try:
            response = self.session.get(
                url=url,
                timeout=self.timeout,
                verify=self.verify_ssl,
                allow_redirects=self.allow_redirects,
            )

            elapsed_ms = round(
                (perf_counter() - start_time) * 1000,
                2,
            )

            return {
                "success": True,
                "response": response,
                "elapsed_ms": elapsed_ms,
                "error": None,
            }

        except RequestException as exc:

            elapsed_ms = round(
                (perf_counter() - start_time) * 1000,
                2,
            )

            return {
                "success": False,
                "response": None,
                "elapsed_ms": elapsed_ms,
                "error": str(exc),
            }

    def close(self) -> None:
        """
        Close the underlying HTTP session.
        """
        self.session.close()