from app import create_app
from app.services import ScanService

app = create_app()

with app.app_context():
    service = ScanService()

    scan = service.run_scan("https://example.com")

    print(scan.id)
    print(scan.status)
    print(scan.score)
    print(scan.grade)