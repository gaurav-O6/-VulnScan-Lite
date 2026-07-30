from flask import Blueprint, jsonify

health_bp = Blueprint(
    "health",
    __name__,
    url_prefix="/api/v1",
)


@health_bp.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    """

    return jsonify(
        {
            "status": "healthy",
            "application": "VulnScan Lite",
            "version": "1.0.0",
        }
    ), 200