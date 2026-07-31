from urllib.parse import urlparse, urlunparse
import ipaddress
import socket


class URLValidator:
    """
    Validates and normalizes scan targets.
    """

    ALLOWED_SCHEMES = {"http", "https"}

    def validate(self, url: str) -> dict:
        """
        Validate and normalize a URL.

        Returns:
            {
                "valid": bool,
                "normalized_url": str | None,
                "error": str | None
            }
        """

        if not url or not url.strip():
            return self._error("URL cannot be empty.")

        url = url.strip()

        parsed = urlparse(url)

        if parsed.scheme.lower() not in self.ALLOWED_SCHEMES:
            return self._error("Only HTTP and HTTPS URLs are supported.")

        if not parsed.netloc:
            return self._error("Invalid URL.")

        hostname = parsed.hostname

        if hostname is None:
            return self._error("Invalid hostname.")

        if hostname.lower() == "localhost":
            return self._error("Localhost is not allowed.")

        try:
            ip = ipaddress.ip_address(hostname)

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_reserved
                or ip.is_multicast
                or ip.is_link_local
            ):
                return self._error(
                    "Private or local IP addresses are not allowed."
                )

        except ValueError:
            # Hostname is not a direct IP address.
            pass

        normalized = self._normalize(parsed)

        return {
            "valid": True,
            "normalized_url": normalized,
            "error": None,
        }

    def _normalize(self, parsed) -> str:
        """
        Normalize a parsed URL.
        """

        scheme = parsed.scheme.lower()

        hostname = parsed.hostname.lower()

        port = parsed.port

        if port:
            if (scheme == "http" and port != 80) or (
                scheme == "https" and port != 443
            ):
                netloc = f"{hostname}:{port}"
            else:
                netloc = hostname
        else:
            netloc = hostname

        path = parsed.path or "/"

        return urlunparse(
            (
                scheme,
                netloc,
                path,
                "",
                "",
                "",
            )
        )

    @staticmethod
    def _error(message: str) -> dict:
        return {
            "valid": False,
            "normalized_url": None,
            "error": message,
        }