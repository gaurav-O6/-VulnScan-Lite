# VulnScan Lite

## Passive Web Vulnerability Scanner

VulnScan Lite is an on-demand passive web security assessment platform that analyzes websites for common security misconfigurations.

The application allows users to submit a website URL and receive a security health report containing:

- Security score
- Risk rating
- Passed and failed security checks
- Vulnerability findings
- Impact explanations
- Remediation recommendations
- Downloadable PDF reports

VulnScan Lite is designed as a safe security assessment tool that performs **passive analysis only** and does not execute aggressive attacks or exploitation attempts.

---

# Disclaimer

⚠️ **Only scan websites you own or have explicit permission to test.**

VulnScan Lite performs passive security analysis by examining:

- HTTP response headers
- SSL/TLS certificate information
- HTML content
- Publicly accessible resources
- Server metadata

It does not perform:

- Exploit attempts
- Vulnerability exploitation
- Brute-force attacks
- Intrusive scanning

---

# Project Overview

Modern websites often contain security misconfigurations such as:

- Missing security headers
- Weak cookie settings
- Exposed server information
- Incorrect HTTPS configuration
- Publicly accessible sensitive files

VulnScan Lite helps identify these issues and provides actionable recommendations to improve security posture.

---

# Features

## Scanner Engine

The scanner engine is implemented as a dedicated Python package:


backend/app/scanner/


Implemented security analysis modules:

- HTTP response analysis
- Security header inspection
- SSL/TLS inspection
- CMS detection
- Cookie security analysis
- HTTP method analysis
- Sensitive file exposure checks
- robots.txt analysis
- security.txt detection
- Response metadata analysis

---

# System Architecture

```text
                         React Frontend
                               |
                               |
                               v
                         Flask API Server
                               |
                               |
                    Create Scan Request
                               |
                               v
                         Redis Queue
                               |
                               |
                               v
                      Background Worker
                               |
                               |
                               v
                    Scanner Engine Modules

        ------------------------------------------------
        |              |              |                |
     Headers          SSL           CMS          Exposure Checks

                               |
                               |
                               v

                    Finding Normalization

                               |
                               |
                               v

                    Security Score Engine

                               |
                               |
                               v

                    Report + PDF Generator
Technology Stack
Backend
Python 3.10
Flask
Flask SQLAlchemy
Flask-Migrate
Redis
RQ Worker
Requests
BeautifulSoup4
ReportLab
Flask-Limiter
Frontend
React
Vite
Axios
Recharts
Database
PostgreSQL
SQLite development support
Scanner Modules
1. Security Header Analysis

The scanner analyzes important HTTP security headers.

Checked headers:

Header	Purpose
Content-Security-Policy	Helps prevent XSS and content injection attacks
Strict-Transport-Security	Enforces HTTPS usage
X-Frame-Options	Protects against clickjacking
X-Content-Type-Options	Prevents MIME sniffing
Referrer-Policy	Controls referrer information leakage
Permissions-Policy	Restricts browser features

Missing security headers generate findings with:

Severity level
Security impact
Remediation guidance
2. SSL/TLS Inspection

The SSL module analyzes HTTPS configuration.

Checks include:

Certificate validity
Certificate expiration
Certificate issuer
TLS connection details
Encryption configuration information
3. CMS Detection

VulnScan Lite performs passive CMS identification.

Detection sources include:

HTML Signatures

Examples:

WordPress
wordpress
wp-content
wp-includes
Drupal
drupal
Joomla
joomla
HTML Metadata

The scanner checks:

<meta name="generator">

for CMS and framework information.

HTTP Headers

Technology disclosure headers are analyzed:

Server
X-Powered-By
4. Cookie Security Analysis

Cookies are analyzed for security attributes:

Secure flag
HttpOnly flag
SameSite attribute

Missing protections generate recommendations.

5. Exposure Checks

The scanner checks for publicly accessible resources:

Sensitive files
Backup files
Configuration files
Common exposed paths
6. HTTP Method Analysis

The scanner checks available HTTP methods.

Potentially unnecessary methods:

TRACE
PUT
DELETE

are analyzed.

7. robots.txt Analysis

The scanner checks:

/robots.txt

for potentially sensitive paths or exposed directories.

8. security.txt Analysis

The scanner checks:

/.well-known/security.txt

for vulnerability disclosure information.

Security Finding Format

All scanner results are normalized into a standard finding structure.

Example:

{
    "category": "headers",
    "name": "Content-Security-Policy",
    "severity": "High",
    "status": "failed",
    "description": "Missing security header",
    "impact": "Increased XSS exposure",
    "recommendation": "Implement CSP header"
}
Security Scoring System

Every scan starts with:

Score = 100

Severity deductions:

Severity	Deduction
Critical	-20
High	-10
Medium	-5
Low	-2
Informational	0

Grade calculation:

Score	Grade
90-100	A
80-89	B
70-79	C
60-69	D
Below 60	F
Async Scan Architecture

Scanning operations run asynchronously to prevent blocking the web server.

Workflow:

User submits website URL
Flask validates the request
Scan record is created
Job is pushed into Redis queue
Background worker executes scanner modules
Findings are generated
Security score is calculated
Report is stored
Frontend polls scan status
Results are displayed
API Endpoints
Create Scan
POST /api/scans

Request:

{
    "url": "https://example.com"
}
Get Scan Status
GET /api/scans/<scan_id>

Returns:

Scan status
Progress
Current stage
Security score
Grade
Findings
Report data
Scan History
GET /api/scans

Returns previous scan results.

Download PDF Report
GET /api/scans/<scan_id>/report/pdf

Generates a professional PDF security report.

Frontend Features

The React dashboard provides:

Website scan submission
Live scan progress tracking
Security score visualization
Findings dashboard
Scan history
PDF report download
Security Controls Implemented

Implemented security best practices:

Passive-only scanning model
URL validation
API rate limiting
Safe HTTP requests
Background job processing
Standardized findings
Error handling
Security recommendations
Local Development
Backend Setup

Create virtual environment:

python -m venv .venv

Activate environment:

Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run backend:

python run.py
Frontend Setup

Install dependencies:

npm install

Start development server:

npm run dev
Docker Support

Docker Compose configuration is included for running required services.

Services:

Backend API
Database
Redis

Run:

docker compose up
Project Structure
VulnScanLite

├── backend
│   ├── app
│   │   ├── api
│   │   ├── models
│   │   ├── scanner
│   │   │   ├── checks
│   │   │   ├── scoring.py
│   │   │   ├── report_builder.py
│   │   │   └── pdf_report_builder.py
│   │   ├── services
│   │   └── workers
│
├── frontend
│   ├── src
│   └── components
│
└── docker-compose.yml
Future Improvements

Possible future enhancements:

User authentication
Multi-user scan isolation
Scheduled scans
Expanded CMS fingerprint database
Additional security checks
Cloud deployment scaling
Project Status

VulnScan Lite implements a complete passive website security assessment workflow:

URL Input
    |
Validation
    |
Async Queue
    |
Scanner Engine
    |
Security Checks
    |
Score Calculation
    |
Report Generation
    |
PDF Export

Built as a cybersecurity engineering internship project.


This version is aligned with the internship description without overclaiming features you don't actually hav