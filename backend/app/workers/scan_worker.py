from datetime import datetime

from app.extensions import db
from app.models import Scan
from app.scanner.scanner import Scanner


def process_scan(scan_id):
    """
    Background worker task.

    Executes vulnerability scan asynchronously
    and updates scan status/results in database.
    """


    # Import here to avoid circular import
    from app import create_app


    app = create_app()


    with app.app_context():

        scan = db.session.get(
            Scan,
            scan_id,
        )


        if scan is None:

            print(
                f"[WORKER] Scan {scan_id} not found."
            )

            return



        scanner = Scanner()


        try:

            print(
                f"[WORKER] Starting scan {scan_id}"
            )


            scan.status = "running"

            scan.started_at = datetime.utcnow()

            db.session.commit()



            result = scanner.scan(
                scan.target_url
            )



            if not result["success"]:

                print(
                    f"[WORKER] Scan {scan_id} failed: "
                    f"{result['error']}"
                )


                scan.status = "failed"

                scan.completed_at = datetime.utcnow()

                db.session.commit()


                return



            report = result["report"]


            scan.report_json = report


            scan.score = (
                report["security_score"]["score"]
            )


            scan.grade = (
                report["security_score"]["grade"]
            )


            scan.status = "completed"

            scan.completed_at = datetime.utcnow()


            db.session.commit()



            print(
                f"[WORKER] Scan {scan_id} completed successfully "
                f"Score={scan.score} Grade={scan.grade}"
            )



        except Exception as e:


            print(
                f"[WORKER ERROR] Scan {scan_id} failed: {e}"
            )


            scan.status = "failed"

            scan.completed_at = datetime.utcnow()


            db.session.commit()


            raise



        finally:

            scanner.close()