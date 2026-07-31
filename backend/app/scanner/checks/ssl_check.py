import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlparse


class SSLChecker:
    """
    Performs passive SSL/TLS certificate inspection.
    """

    DEFAULT_PORT = 443

    def analyze(self, context: dict) -> dict:
        """
        Analyze the target's SSL certificate.

        Args:
            context:
                {
                    "url": "...",
                    "response": requests.Response
                }

        Returns:
            Dictionary containing SSL inspection results.
        """

        url = context["url"]

        parsed = urlparse(url)

        if parsed.scheme != "https":
            return {
                "enabled": False,
                "valid": False,
                "subject": None,
                "issuer": None,
                "expires_on": None,
                "days_remaining": None,
                "error": "Target does not use HTTPS.",
            }

        hostname = parsed.hostname
        port = parsed.port or self.DEFAULT_PORT

        try:

            ssl_context = ssl.create_default_context()

            with socket.create_connection((hostname, port), timeout=10) as sock:

                with ssl_context.wrap_socket(
                    sock,
                    server_hostname=hostname,
                ) as secure_socket:

                    certificate = secure_socket.getpeercert()

            expires_string = certificate["notAfter"]

            expires_on = datetime.strptime(
                expires_string,
                "%b %d %H:%M:%S %Y %Z",
            ).replace(tzinfo=timezone.utc)

            now = datetime.now(timezone.utc)

            days_remaining = (expires_on - now).days

            subject = dict(
                item
                for group in certificate.get("subject", [])
                for item in group
            )

            issuer = dict(
                item
                for group in certificate.get("issuer", [])
                for item in group
            )

            return {
                "enabled": True,
                "valid": days_remaining >= 0,
                "subject": subject,
                "issuer": issuer,
                "expires_on": expires_on.isoformat(),
                "days_remaining": days_remaining,
                "error": None,
            }

        except Exception as exc:

            return {
                "enabled": True,
                "valid": False,
                "subject": None,
                "issuer": None,
                "expires_on": None,
                "days_remaining": None,
                "error": str(exc),
            }