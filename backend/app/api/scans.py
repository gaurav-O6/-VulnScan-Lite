from flask import Blueprint, jsonify, request

from app.services import ScanService


scans_bp = Blueprint(
    "scans",
    __name__,
    url_prefix="/api/scans",
)


@scans_bp.route("", methods=["POST"])
def create_scan():
    """
    Create and execute a vulnerability scan.
    """

    data = request.get_json(silent=True)

    if data is None:
        return (
            jsonify(
                {
                    "error": "Request body must be valid JSON."
                }
            ),
            400,
        )

    url = data.get("url")

    if not url:
        return (
            jsonify(
                {
                    "error": "Field 'url' is required."
                }
            ),
            400,
        )

    service = ScanService()

    scan = service.run_scan(url)

    return (
        jsonify(
            {
                "scan_id": scan.id,
                "status": scan.status,
            }
        ),
        201,
    )


@scans_bp.route("/<int:scan_id>", methods=["GET"])
def get_scan(scan_id: int):
    """
    Retrieve a stored scan.
    """

    service = ScanService()

    scan = service.get_scan(scan_id)

    if scan is None:
        return (
            jsonify(
                {
                    "error": "Scan not found."
                }
            ),
            404,
        )

    return jsonify(
        {
            "id": scan.id,
            "target_url": scan.target_url,
            "status": scan.status,
            "score": scan.score,
            "grade": scan.grade,
            "ssl_valid": scan.ssl_valid,
            "ssl_expiry": scan.ssl_expiry,
            "cms_name": scan.cms_name,
            "cms_version": scan.cms_version,
            "headers": scan.headers_json,
            "findings": scan.findings_json,
            "remediation": scan.remediation_json,
            "created_at": (
                scan.created_at.isoformat()
                if scan.created_at
                else None
            ),
            "started_at": (
                scan.started_at.isoformat()
                if scan.started_at
                else None
            ),
            "completed_at": (
                scan.completed_at.isoformat()
                if scan.completed_at
                else None
            ),
        }
    )