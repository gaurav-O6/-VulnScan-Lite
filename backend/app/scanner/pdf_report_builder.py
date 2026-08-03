from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


#
# Register Unicode font when available.
#

try:
    pdfmetrics.registerFont(
        TTFont(
            "DejaVu",
            "DejaVuSans.ttf",
        )
    )

    DEFAULT_FONT = "DejaVu"

except Exception:

    DEFAULT_FONT = "Helvetica"


class PDFReportBuilder:
    """
    Generates a professional PDF security assessment report
    from a completed VulnScan Lite scan.
    """

    def __init__(self):

        self.styles = getSampleStyleSheet()

        self.title_style = ParagraphStyle(
            "Title",
            parent=self.styles["Heading1"],
            alignment=TA_CENTER,
            fontName=DEFAULT_FONT,
            fontSize=24,
            spaceAfter=20,
            textColor=colors.HexColor("#0b5ed7"),
        )

        self.heading_style = ParagraphStyle(
            "Heading",
            parent=self.styles["Heading2"],
            fontName=DEFAULT_FONT,
            fontSize=16,
            spaceBefore=12,
            spaceAfter=10,
            textColor=colors.HexColor("#1f2937"),
        )

        self.subheading_style = ParagraphStyle(
            "SubHeading",
            parent=self.styles["Heading3"],
            fontName=DEFAULT_FONT,
            fontSize=13,
            spaceBefore=8,
            spaceAfter=6,
        )

        self.normal_style = ParagraphStyle(
            "NormalText",
            parent=self.styles["BodyText"],
            fontName=DEFAULT_FONT,
            fontSize=10,
            leading=16,
        )

        self.small_style = ParagraphStyle(
            "Small",
            parent=self.styles["BodyText"],
            fontName=DEFAULT_FONT,
            fontSize=8,
            leading=11,
            textColor=colors.grey,
        )

    def build(
        self,
        scan,
    ):
        """
        Generate PDF bytes from a completed scan.
        """

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=(8.5 * inch, 11 * inch),
            leftMargin=0.55 * inch,
            rightMargin=0.55 * inch,
            topMargin=0.60 * inch,
            bottomMargin=0.60 * inch,
        )

        story = []

        report = scan.report_json or {}

        self._build_cover(
            story,
            scan,
            report,
        )

        self._build_executive_summary(
            story,
            report,
        )

        self._build_scan_information(
            story,
            scan,
            report,
        )

        story.append(PageBreak())

        self._build_security_overview(
            story,
            report,
        )

        self._build_findings_summary(
            story,
            report,
        )

        self._build_passed_checks(
            story,
            report,
        )

        self._build_failed_checks(
            story,
            report,
        )

        self._build_recommendations(
            story,
            report,
        )

        self._build_footer(
            story,
        )

        document.build(story)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf

    def _build_cover(
        self,
        story,
        scan,
        report,
    ):

        story.append(
            Paragraph(
                "VulnScan Lite",
                self.title_style,
            )
        )

        story.append(
            Paragraph(
                "Passive Web Security Assessment Report",
                self.heading_style,
            )
        )

        story.append(
            Spacer(
                1,
                0.25 * inch,
            )
        )

        score = report.get(
            "security_score",
            {},
        )

        metadata = report.get(
            "metadata",
            {},
        )

        table = Table(
            [
                [
                    "Target",
                    scan.target_url,
                ],
                [
                    "Security Score",
                    str(
                        score.get(
                            "score",
                            0,
                        )
                    ),
                ],
                [
                    "Grade",
                    score.get(
                        "grade",
                        "F",
                    ),
                ],
                [
                    "Status",
                    scan.status.title(),
                ],
                [
                    "Generated",
                    metadata.get(
                        "generated_at",
                        datetime.utcnow().isoformat(),
                    ),
                ],
            ],
            colWidths=[
                2.0 * inch,
                4.6 * inch,
            ],
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#0b5ed7"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (0, -1),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, -1),
                        DEFAULT_FONT,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.grey,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                ]
            )
        )

        story.append(table)

        story.append(
            Spacer(
                1,
                0.30 * inch,
            )
        )

    def _build_executive_summary(
        self,
        story,
        report,
    ):
        """
        Executive summary section.
        """

        story.append(
            Paragraph(
                "Executive Summary",
                self.heading_style,
            )
        )

        executive = report.get(
            "executive_summary",
            {},
        )

        headline = executive.get(
            "headline",
            "Security assessment completed.",
        )

        description = executive.get(
            "description",
            "",
        )

        priority = executive.get(
            "priority",
            "Unknown",
        )

        story.append(
            Paragraph(
                f"<b>{headline}</b>",
                self.normal_style,
            )
        )

        story.append(
            Spacer(
                1,
                0.08 * inch,
            )
        )

        story.append(
            Paragraph(
                description,
                self.normal_style,
            )
        )

        story.append(
            Spacer(
                1,
                0.12 * inch,
            )
        )

        story.append(
            Paragraph(
                f"<b>Overall Risk:</b> {priority}",
                self.normal_style,
            )
        )

        story.append(
            Spacer(
                1,
                0.20 * inch,
            )
        )

    def _build_scan_information(
        self,
        story,
        scan,
        report,
    ):
        """
        Basic scan information.
        """

        story.append(
            Paragraph(
                "Scan Information",
                self.heading_style,
            )
        )

        metadata = report.get(
            "metadata",
            {},
        )

        response_info = report.get(
            "response_info",
            {},
        )

        generated = metadata.get(
            "generated_at",
            "N/A",
        )

        rows = [
            [
                "Target URL",
                scan.target_url,
            ],
            [
                "Scanner",
                metadata.get(
                    "scanner",
                    "VulnScan Lite",
                ),
            ],
            [
                "Version",
                metadata.get(
                    "version",
                    "1.0",
                ),
            ],
            [
                "Generated",
                generated,
            ],
            [
                "HTTP Status",
                str(
                    response_info.get(
                        "status_code",
                        "Unknown",
                    )
                ),
            ],
            [
                "Server",
                response_info.get(
                    "server",
                    "Unknown",
                ),
            ],
            [
                "Content Type",
                response_info.get(
                    "content_type",
                    "Unknown",
                ),
            ],
        ]

        table = Table(
            rows,
            colWidths=[
                2.1 * inch,
                4.5 * inch,
            ],
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#f3f4f6"),
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.35,
                        colors.grey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, -1),
                        DEFAULT_FONT,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ]
            )
        )

        story.append(table)

        story.append(
            Spacer(
                1,
                0.20 * inch,
            )
        )

    def _build_security_overview(
        self,
        story,
        report,
    ):
        """
        Overall score and risk overview.
        """

        story.append(
            Paragraph(
                "Security Overview",
                self.heading_style,
            )
        )

        security = report.get(
            "security_score",
            {},
        )

        overview = report.get(
            "risk_overview",
            {},
        )

        summary = report.get(
            "summary",
            {},
        )

        rows = [
            [
                "Security Score",
                f"{security.get('score', 0)}/100",
            ],
            [
                "Grade",
                security.get(
                    "grade",
                    "F",
                ),
            ],
            [
                "Overall Risk",
                overview.get(
                    "overall_risk",
                    "Unknown",
                ),
            ],
            [
                "Highest Severity",
                overview.get(
                    "highest_severity",
                    "None",
                ),
            ],
            [
                "Critical Findings",
                str(
                    summary.get(
                        "critical",
                        0,
                    )
                ),
            ],
            [
                "High Findings",
                str(
                    summary.get(
                        "high",
                        0,
                    )
                ),
            ],
            [
                "Medium Findings",
                str(
                    summary.get(
                        "medium",
                        0,
                    )
                ),
            ],
            [
                "Low Findings",
                str(
                    summary.get(
                        "low",
                        0,
                    )
                ),
            ],
        ]

        table = Table(
            rows,
            colWidths=[
                2.4 * inch,
                3.9 * inch,
            ],
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.grey,
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#e5e7eb"),
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, -1),
                        DEFAULT_FONT,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ]
            )
        )

        story.append(table)

        story.append(
            Spacer(
                1,
                0.20 * inch,
            )
        )

    def _build_findings_summary(
        self,
        story,
        report,
    ):
        """
        High-level findings summary.
        """

        story.append(
            Paragraph(
                "Findings Summary",
                self.heading_style,
            )
        )

        summary = report.get(
            "summary",
            {},
        )

        table = Table(
            [
                [
                    "Total",
                    "Critical",
                    "High",
                    "Medium",
                    "Low",
                    "Informational",
                ],
                [
                    summary.get(
                        "total_findings",
                        0,
                    ),
                    summary.get(
                        "critical",
                        0,
                    ),
                    summary.get(
                        "high",
                        0,
                    ),
                    summary.get(
                        "medium",
                        0,
                    ),
                    summary.get(
                        "low",
                        0,
                    ),
                    summary.get(
                        "informational",
                        0,
                    ),
                ],
            ],
            colWidths=[
                0.9 * inch,
                1.0 * inch,
                0.9 * inch,
                1.0 * inch,
                0.8 * inch,
                1.2 * inch,
            ],
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#0b5ed7"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.grey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, -1),
                        DEFAULT_FONT,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                ]
            )
        )

        story.append(table)

        story.append(
            Spacer(
                1,
                0.25 * inch,
            )
        ) 

    def _build_passed_checks(
        self,
        story,
        report,
    ):
        """
        Display successful security checks.
        """

        story.append(
            Paragraph(
                "Successful Security Checks",
                self.heading_style,
            )
        )

        findings = report.get(
            "findings",
            [],
        )

        passed = [
            finding
            for finding in findings
            if finding.get("status") == "passed"
        ]

        if not passed:

            story.append(
                Paragraph(
                    "No successful checks were recorded.",
                    self.normal_style,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.15 * inch,
                )
            )

            return

        rows = [
            [
                "Check",
                "Severity",
            ]
        ]

        for finding in passed:

            rows.append(
                [
                    finding.get(
                        "title",
                        finding.get(
                            "name",
                            "Unknown",
                        ),
                    ),
                    finding.get(
                        "severity",
                        "-",
                    ),
                ]
            )

        table = Table(
            rows,
            colWidths=[
                5.2 * inch,
                1.2 * inch,
            ],
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#198754"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.35,
                        colors.grey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, -1),
                        DEFAULT_FONT,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ]
            )
        )

        story.append(table)

        story.append(
            Spacer(
                1,
                0.25 * inch,
            )
        )

    def _build_failed_checks(
        self,
        story,
        report,
    ):
        """
        Display failed security findings.
        """

        story.append(
            Paragraph(
                "Detailed Security Findings",
                self.heading_style,
            )
        )

        findings = report.get(
            "findings",
            [],
        )

        failed = [
            finding
            for finding in findings
            if finding.get("status") == "failed"
        ]

        if not failed:

            story.append(
                Paragraph(
                    "No failed security checks were identified.",
                    self.normal_style,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.15 * inch,
                )
            )

            return

        for finding in failed:

            title = finding.get(
                "title",
                finding.get(
                    "name",
                    "Unknown Finding",
                ),
            )

            severity = finding.get(
                "severity",
                "Low",
            )

            story.append(
                Paragraph(
                    f"<b>{title}</b>",
                    self.subheading_style,
                )
            )

            info = Table(
                [
                    [
                        "Severity",
                        severity,
                    ],
                    [
                        "Category",
                        finding.get(
                            "category",
                            "-",
                        ),
                    ],
                    [
                        "Description",
                        finding.get(
                            "description",
                            "-",
                        ),
                    ],
                    [
                        "Impact",
                        finding.get(
                            "impact",
                            "-",
                        ),
                    ],
                    [
                        "Evidence",
                        str(
                            finding.get(
                                "evidence",
                                "-",
                            )
                        ),
                    ],
                ],
                colWidths=[
                    1.6 * inch,
                    4.8 * inch,
                ],
            )

            info.setStyle(
                TableStyle(
                    [
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.3,
                            colors.grey,
                        ),
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, -1),
                            colors.HexColor("#f3f4f6"),
                        ),
                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, -1),
                            DEFAULT_FONT,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            6,
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            6,
                        ),
                    ]
                )
            )

            story.append(info)

            recommendation = finding.get(
                "recommendation"
            )

            if recommendation:

                story.append(
                    Spacer(
                        1,
                        0.05 * inch,
                    )
                )

                story.append(
                    Paragraph(
                        f"<b>Recommendation:</b> {recommendation}",
                        self.normal_style,
                    )
                )

            reference = finding.get(
                "reference"
            )

            if reference:

                story.append(
                    Paragraph(
                        f"<b>Reference:</b> {reference}",
                        self.small_style,
                    )
                )

            story.append(
                Spacer(
                    1,
                    0.18 * inch,
                )
            )

    def _build_recommendations(
        self,
        story,
        report,
    ):
        """
        Display remediation recommendations.
        """

        story.append(
            Paragraph(
                "Prioritized Recommendations",
                self.heading_style,
            )
        )

        recommendations = report.get(
            "recommendations",
            [],
        )

        if not recommendations:

            story.append(
                Paragraph(
                    "No recommendations available.",
                    self.normal_style,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.20 * inch,
                )
            )

            return

        for index, recommendation in enumerate(
            recommendations,
            start=1,
        ):

            story.append(
                Paragraph(
                    f"{index}. {recommendation}",
                    self.normal_style,
                )
            )

        story.append(
            Spacer(
                1,
                0.25 * inch,
            )
        )

    def _build_footer(
        self,
        story,
    ):
        """
        Footer disclaimer.
        """

        story.append(
            Spacer(
                1,
                0.35 * inch,
            )
        )

        story.append(
            Paragraph(
                "Disclaimer",
                self.heading_style,
            )
        )

        story.append(
            Paragraph(
                (
                    "This report was generated automatically by "
                    "VulnScan Lite using passive security analysis. "
                    "The results should be reviewed by a security "
                    "professional before making production security "
                    "decisions. A passive assessment cannot identify "
                    "every possible vulnerability."
                ),
                self.normal_style,
            )
        )

        story.append(
            Spacer(
                1,
                0.20 * inch,
            )
        )

        story.append(
            Paragraph(
                (
                    f"Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} "
                    "by VulnScan Lite v1.0"
                ),
                self.small_style,
            )
        )