from dataclasses import dataclass, asdict


@dataclass
class Finding:
    """
    Standard security finding format.
    """

    id: str
    category: str
    name: str
    severity: str
    status: str
    description: str
    evidence: object = None
    recommendation: str = None


def normalize_finding(
    finding: dict,
    category: str,
    finding_id: str,
) -> dict:
    """
    Convert old checker finding format
    into standardized finding format.
    """

    return asdict(
        Finding(
            id=finding_id,
            category=category,
            name=finding.get(
                "name",
                "Unknown Finding",
            ),
            severity=finding.get(
                "severity",
                "Low",
            ),
            status=finding.get(
                "status",
                "unknown",
            ),
            description=finding.get(
                "description",
                "",
            ),
            evidence=finding.get(
                "value"
            ),
            recommendation=get_recommendation(
                finding.get("name", "")
            ),
        )
    )


def get_recommendation(name: str) -> str:
    """
    Generate basic remediation advice.
    """

    name = name.lower()


    if "cookie" in name:
        return (
            "Configure secure cookie attributes "
            "such as HttpOnly, Secure, and SameSite."
        )


    if "header" in name:
        return (
            "Configure recommended security headers "
            "on the web server."
        )


    if "file" in name:
        return (
            "Remove sensitive files from public "
            "web directories."
        )


    if "robots" in name:
        return (
            "Avoid exposing sensitive paths "
            "through robots.txt."
        )


    if "security.txt" in name:
        return (
            "Publish a security.txt file "
            "for vulnerability disclosure."
        )


    if "method" in name:
        return (
            "Disable unnecessary HTTP methods."
        )


    return (
        "Review this security finding "
        "and apply appropriate remediation."
    )