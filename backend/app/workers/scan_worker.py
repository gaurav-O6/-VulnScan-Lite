from datetime import datetime
import logging


from app.extensions import db
from app.models import Scan
from app.scanner.scanner import Scanner


logger = logging.getLogger(__name__)


def update_progress(
    scan,
    progress,
    stage,
):
    """
    Update scan progress safely.
    """

    scan.progress = progress
    scan.current_stage = stage

    db.session.commit()



def process_scan(scan_id):
    """
    Background worker task.

    Executes vulnerability scan asynchronously
    and updates scan status/results in database.
    """

    from app import create_app


    app = create_app()

    scanner = None


    with app.app_context():


        scan = db.session.get(
            Scan,
            scan_id,
        )


        if scan is None:

            logger.warning(
                "Scan %s not found.",
                scan_id,
            )

            return



        try:


            scanner = Scanner()


            logger.info(
                "Starting scan %s",
                scan_id,
            )



            scan.status = "running"

            scan.started_at = datetime.utcnow()



            update_progress(
                scan,
                5,
                "Initializing scanner",
            )



            update_progress(
                scan,
                15,
                "Validating target URL",
            )



            update_progress(
                scan,
                30,
                "Running security checks",
            )



            result = scanner.scan(
                scan.target_url
            )



            update_progress(
                scan,
                85,
                "Analyzing findings",
            )



            if not result["success"]:


                logger.warning(
                    "Scan %s failed: %s",
                    scan_id,
                    result["error"],
                )



                scan.status = "failed"



                scan.report_json = {
                    "error": result["error"],
                    "target": scan.target_url,
                }



                scan.completed_at = datetime.utcnow()



                update_progress(
                    scan,
                    100,
                    "Scan failed",
                )



                return



            update_progress(
                scan,
                95,
                "Building final report",
            )



            report = result["report"]



            scan.report_json = report



            scan.score = (
                report
                .get(
                    "security_score",
                    {},
                )
                .get(
                    "score",
                    0,
                )
            )



            scan.grade = (
                report
                .get(
                    "security_score",
                    {},
                )
                .get(
                    "grade",
                    "F",
                )
            )



            scan.status = "completed"



            scan.completed_at = datetime.utcnow()



            update_progress(
                scan,
                100,
                "Completed",
            )



            logger.info(
                "Scan %s completed. Score=%s Grade=%s",
                scan_id,
                scan.score,
                scan.grade,
            )



        except Exception:


            logger.exception(
                "Scan %s failed unexpectedly.",
                scan_id,
            )



            scan.status = "failed"



            scan.report_json = {
                "error": "Internal scan processing error.",
                "target": scan.target_url,
            }



            scan.completed_at = datetime.utcnow()



            update_progress(
                scan,
                100,
                "Failed",
            )



            raise



        finally:


            if scanner:

                scanner.close()