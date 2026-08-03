from datetime import datetime

from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Scan

from app.queue import scan_queue
from app.workers.scan_worker import process_scan


scans_bp = Blueprint(
    "scans",
    __name__,
    url_prefix="/api/scans",
)


def get_risk_level(score: int) -> str:
    """
    Convert security score into risk category.
    """

    if score >= 90:
        return "Low"

    if score >= 70:
        return "Medium"

    if score >= 50:
        return "High"

    return "Critical"



def calculate_duration(scan: Scan):
    """
    Calculate scan execution duration.
    """

    if (
        scan.started_at
        and scan.completed_at
    ):

        duration = (
            scan.completed_at
            - scan.started_at
        )

        return round(
            duration.total_seconds(),
            2,
        )

    return None



@scans_bp.route("", methods=["POST"])
def create_scan():
    """
    Queue a vulnerability scan.
    """

    data = request.get_json(
        silent=True
    )

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


    scan = Scan(
        target_url=url,
        status="queued",
        started_at=None,
        completed_at=None,
    )


    db.session.add(scan)

    db.session.commit()



    scan_queue.enqueue(
        process_scan,
        scan.id,
    )


    return (
        jsonify(
            {
                "scan_id": scan.id,
                "status": scan.status,
            }
        ),
        201,
    )



@scans_bp.route(
    "/<int:scan_id>",
    methods=["GET"],
)
def get_scan(scan_id: int):
    """
    Retrieve scan result.
    """


    scan = db.session.get(
        Scan,
        scan_id,
    )


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

            "risk_level": get_risk_level(
                scan.score
            ),

            "duration_seconds": calculate_duration(
                scan
            ),

            "report": scan.report_json,

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



@scans_bp.route(
    "",
    methods=["GET"],
)
def get_scan_history():
    """
    Retrieve scan history.
    """


    scans = (
        Scan.query
        .order_by(
            Scan.created_at.desc()
        )
        .all()
    )


    history = []


    for scan in scans:


        findings_count = 0


        if isinstance(
            scan.report_json,
            dict,
        ):

            findings = scan.report_json.get(
                "findings",
                [],
            )


            if isinstance(
                findings,
                list,
            ):

                findings_count = len(
                    findings
                )



        history.append(
            {
                "id": scan.id,

                "target_url": scan.target_url,

                "status": scan.status,

                "score": scan.score,

                "grade": scan.grade,

                "risk_level": get_risk_level(
                    scan.score
                ),

                "findings_count": findings_count,

                "duration_seconds": calculate_duration(
                    scan
                ),

                "created_at": (
                    scan.created_at.isoformat()
                    if scan.created_at
                    else None
                ),

                "completed_at": (
                    scan.completed_at.isoformat()
                    if scan.completed_at
                    else None
                ),
            }
        )


    return jsonify(history)



@scans_bp.route(
    "/<int:scan_id>",
    methods=["DELETE"],
)
def delete_scan(scan_id: int):
    """
    Delete scan history entry.
    """


    scan = db.session.get(
        Scan,
        scan_id,
    )


    if scan is None:

        return (
            jsonify(
                {
                    "error": "Scan not found."
                }
            ),
            404,
        )


    db.session.delete(
        scan
    )

    db.session.commit()


    return jsonify(
        {
            "message": "Scan deleted successfully.",
            "scan_id": scan_id,
        }
    )