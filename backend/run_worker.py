from rq import SimpleWorker

from app import create_app
from app.queue import scan_queue, redis_connection


app = create_app()


with app.app_context():

    print(
        "VulnScanLite worker started"
    )

    worker = SimpleWorker(
        [scan_queue],
        connection=redis_connection,
    )

    worker.work()