from urllib.parse import urlparse, urlunparse

import ipaddress
import socket


class URLValidator:
    """
    Validates and normalizes scan targets.

    Includes SSRF protection by preventing
    access to local/private network targets.
    """


    ALLOWED_SCHEMES = {
        "http",
        "https",
    }


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

            return self._error(
                "URL cannot be empty."
            )


        url = url.strip()


        if len(url) > 2048:

            return self._error(
                "URL is too long."
            )


        parsed = urlparse(url)


        if parsed.scheme.lower() not in self.ALLOWED_SCHEMES:

            return self._error(
                "Only HTTP and HTTPS URLs are supported."
            )


        if not parsed.netloc:

            return self._error(
                "Invalid URL."
            )


        hostname = parsed.hostname


        if hostname is None:

            return self._error(
                "Invalid hostname."
            )


        hostname = hostname.lower()



        if hostname == "localhost":

            return self._error(
                "Localhost is not allowed."
            )



        if not self._is_safe_ip(hostname):

            return self._error(
                "Private or local IP addresses are not allowed."
            )



        if not self._resolves_to_public_ip(hostname):

            return self._error(
                "Target resolves to a private or local IP address."
            )



        normalized = self._normalize(parsed)


        return {
            "valid": True,
            "normalized_url": normalized,
            "error": None,
        }



    def _is_safe_ip(self, hostname: str) -> bool:
        """
        Validate direct IP addresses.
        """


        try:

            ip = ipaddress.ip_address(
                hostname
            )


            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_reserved
                or ip.is_multicast
                or ip.is_link_local
            ):

                return False


        except ValueError:

            # Hostname, not direct IP.
            pass


        return True



    def _resolves_to_public_ip(self, hostname: str) -> bool:
        """
        Prevent DNS based SSRF attacks.

        Resolves hostname and verifies
        returned addresses are public.
        """


        try:

            addresses = socket.gethostbyname_ex(
                hostname
            )[2]


            for address in addresses:

                ip = ipaddress.ip_address(
                    address
                )


                if (
                    ip.is_private
                    or ip.is_loopback
                    or ip.is_reserved
                    or ip.is_multicast
                    or ip.is_link_local
                ):

                    return False



        except socket.gaierror:

            return False


        return True



    def _normalize(self, parsed) -> str:
        """
        Normalize a parsed URL.
        """


        scheme = parsed.scheme.lower()

        hostname = parsed.hostname.lower()

        port = parsed.port


        if port:

            if (
                (scheme == "http" and port != 80)
                or
                (scheme == "https" and port != 443)
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