from dataclasses import dataclass, asdict


SEVERITY_MAP = {
    "critical": "Critical",
    "high": "High",
    "medium": "Medium",
    "low": "Low",
    "informational": "Informational",
    "info": "Informational",
}


@dataclass
class Finding:
    """
    Standard security finding format.
    """

    id: str
    category: str
    name: str
    title: str
    severity: str
    status: str
    description: str
    impact: str = ""
    evidence: object = None
    recommendation: str = None
    reference: str = None


def normalize_finding(
    finding: dict,
    category: str,
    finding_id: str,
) -> dict:
    """
    Convert checker output into the standardized
    finding format while remaining backward-compatible.
    """

    name = finding.get(
        "name",
        "Unknown Finding",
    )

    severity = normalize_severity(
        finding.get(
            "severity",
            "Low",
        )
    )

    return asdict(
        Finding(
            id=finding_id,
            category=category,
            name=name,
            title=name,
            severity=severity,
            status=finding.get(
                "status",
                "unknown",
            ),
            description=finding.get(
                "description",
                "",
            ),
            impact=get_impact(name),
            evidence=finding.get(
                "value"
            ),
            recommendation=get_recommendation(name),
            reference=get_reference(name),
        )
    )


def normalize_severity(severity: str) -> str:
    """
    Normalize severity values to a consistent set.
    """

    if not severity:
        return "Low"

    return SEVERITY_MAP.get(
        severity.strip().lower(),
        "Low",
    )


def get_recommendation(name: str) -> str:
    """
    Generate remediation guidance for common findings.
    """

    name = name.lower()

    if "content-security-policy" in name:
        return (
            "Implement a Content-Security-Policy header to restrict "
            "trusted sources for scripts, styles, images, and other "
            "browser resources."
        )

    if "strict-transport-security" in name:
        return (
            "Enable HTTP Strict Transport Security (HSTS) to force "
            "clients to use HTTPS for future connections."
        )

    if "x-frame-options" in name:
        return (
            "Configure the X-Frame-Options header to DENY or SAMEORIGIN "
            "to reduce clickjacking risk."
        )

    if "x-content-type-options" in name:
        return (
            "Set X-Content-Type-Options to 'nosniff' to prevent browsers "
            "from MIME type sniffing."
        )

    if "referrer-policy" in name:
        return (
            "Configure a Referrer-Policy that limits unnecessary "
            "information disclosure."
        )

    if "permissions-policy" in name:
        return (
            "Restrict browser features using a Permissions-Policy header."
        )

    if "httponly" in name:
        return (
            "Enable the HttpOnly cookie attribute to prevent client-side "
            "scripts from accessing session cookies."
        )

    if "secure cookie" in name:
        return (
            "Enable the Secure cookie attribute so cookies are only sent "
            "over encrypted HTTPS connections."
        )

    if "samesite" in name:
        return (
            "Configure the SameSite cookie attribute to reduce the risk "
            "of Cross-Site Request Forgery (CSRF)."
        )

    if "server header" in name:
        return (
            "Reduce server fingerprinting by minimizing or removing the "
            "Server response header where practical."
        )

    if "x-powered-by" in name:
        return (
            "Disable or obfuscate the X-Powered-By header to reduce "
            "technology disclosure."
        )

    if "method" in name:
        return (
            "Disable unnecessary HTTP methods and only allow methods "
            "required by the application."
        )

    if "robots" in name:
        return (
            "Avoid exposing sensitive directories or administrative "
            "paths through robots.txt."
        )

    if "security.txt" in name:
        return (
            "Publish a security.txt file containing vulnerability "
            "reporting contact information."
        )

    if "sensitive file" in name:
        return (
            "Remove sensitive files from public web directories and "
            "store backups outside the web root."
        )

    if "cookie" in name:
        return (
            "Review cookie security attributes including Secure, "
            "HttpOnly, and SameSite."
        )

    if "header" in name:
        return (
            "Review and configure the recommended HTTP security headers."
        )

    return (
        "Review this finding and apply appropriate security controls "
        "based on your application's requirements."
    )


def get_impact(name: str) -> str:
    """
    Describe why the finding matters.
    """

    name = name.lower()

    if "content-security-policy" in name:
        return "Missing CSP increases exposure to Cross-Site Scripting (XSS) and content injection attacks."

    if "strict-transport-security" in name:
        return "Without HSTS, users may be vulnerable to SSL stripping and protocol downgrade attacks."

    if "x-frame-options" in name:
        return "The application may be vulnerable to clickjacking attacks."

    if "cookie" in name:
        return "Weak cookie protection can increase the risk of session hijacking and CSRF."

    if "server header" in name or "x-powered-by" in name:
        return "Technology disclosure can assist attackers during reconnaissance."

    if "method" in name:
        return "Unnecessary HTTP methods may expand the application's attack surface."

    if "sensitive file" in name:
        return "Exposed files may leak credentials, source code, or sensitive configuration."

    if "robots" in name:
        return "robots.txt may unintentionally advertise sensitive application paths."

    if "security.txt" in name:
        return "The absence of security.txt makes coordinated vulnerability disclosure more difficult."

    return "This issue may reduce the overall security posture of the target."


def get_reference(name: str) -> str:
    """
    Return an authoritative reference where applicable.
    """

    name = name.lower()

    if "content-security-policy" in name:
        return "https://developer.mozilla.org/docs/Web/HTTP/CSP"

    if "strict-transport-security" in name:
        return "https://developer.mozilla.org/docs/Web/HTTP/Headers/Strict-Transport-Security"

    if "x-frame-options" in name:
        return "https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Frame-Options"

    if "x-content-type-options" in name:
        return "https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Content-Type-Options"

    if "referrer-policy" in name:
        return "https://developer.mozilla.org/docs/Web/HTTP/Headers/Referrer-Policy"

    if "permissions-policy" in name:
        return "https://developer.mozilla.org/docs/Web/HTTP/Headers/Permissions-Policy"

    if "cookie" in name:
        return "https://owasp.org/www-community/controls/SecureCookieAttribute"

    if "security.txt" in name:
        return "https://securitytxt.org/"

    return None