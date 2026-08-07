from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from app.reporting.scan_details import create_scan_details
from app.reporting.report_health import create_report_health
from app.reporting.report_version import create_report_version
from app.reporting.system_information import create_system_information
from app.reporting.cost_optimization import create_cost_optimization
from app.reporting.panel_factory import create_panel
from app.reporting.cost_summary import create_cost_table
from app.reporting.report_metadata import create_metadata_table
from app.reporting.audit_status import create_audit_status
from app.reporting.security_score import create_security_score
from app.reporting.risk_summary import create_risk_summary
from app.reporting.resource_summary import create_resource_summary
from app.reporting.report_statistics import create_report_statistics


def create_layout(scan_data):

    layout = Layout(name="root")

    # =========================
    # MAIN LAYOUT
    # =========================

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )

    layout["body"].split_row(
        Layout(name="left", ratio=3),
        Layout(name="right", ratio=2),
    )

    layout["left"].split_column(
        Layout(name="metadata", size=9),
        Layout(name="scan", size=8),
        Layout(name="version", size=8),
        Layout(name="system", size=8),
        Layout(name="health", size=5),
        Layout(name="status", size=5),
        Layout(name="security", size=7),
        Layout(name="risk", size=10),
        Layout(name="resource", size=10),
        Layout(name="statistics", size=10),
        Layout(name="summary"),
        Layout(name="cost"),
        Layout(name="optimization", size=9),
    )

    # =========================
    # HEADER
    # =========================

    layout["header"].update(
        create_panel(
            Text(
                "Cloud Infrastructure Auditor & Cost Optimizer",
                justify="center",
                style="bold cyan",
            )
        )
    )

    # =========================
    # REPORT INFORMATION
    # =========================

    layout["metadata"].update(
        create_panel(
            create_metadata_table(
                scan_data.get("generation_time", 0.0)
            ),
            title="Report Information",
            border_style="magenta",
        )
    )

    # =========================
    # SCAN DETAILS
    # =========================

    layout["scan"].update(
        create_scan_details(scan_data)
    )

    # =========================
    # VERSION INFORMATION
    # =========================

    layout["version"].update(
        create_report_version()
    )

    # =========================
    # SYSTEM INFORMATION
    # =========================

    layout["system"].update(
        create_system_information()
    )

    # =========================
    # ENVIRONMENT HEALTH
    # =========================

    layout["health"].update(
        create_report_health(scan_data)
    )

    # =========================
    # AUDIT STATUS
    # =========================

    layout["status"].update(
        create_audit_status(scan_data)
    )

    # =========================
    # SECURITY SCORE
    # =========================

    layout["security"].update(
        create_security_score(87)
    )

    # =========================
    # RISK SUMMARY
    # =========================

    layout["risk"].update(
        create_risk_summary(scan_data)
    )

    # =========================
    # RESOURCE SUMMARY
    # =========================

    resource_data = {
        "EC2": 8,
        "S3": 6,
        "RDS": 3,
        "Lambda": 5,
        "IAM": 3,
    }

    layout["resource"].update(
        create_resource_summary(resource_data)
    )

    # =========================
    # REPORT STATISTICS
    # =========================

    layout["statistics"].update(
        create_report_statistics()
    )

    # =========================
    # SCAN SUMMARY
    # =========================

    summary_table = Table(
        show_header=True,
        header_style="bold cyan",
        expand=True,
    )

    summary_table.add_column("Metric")
    summary_table.add_column("Value", justify="center")

    summary_table.add_row(
        "Total Resources",
        str(scan_data["total_resources"]),
    )

    summary_table.add_row(
        "Passed",
        str(scan_data["passed"]),
    )

    summary_table.add_row(
        "Warnings",
        str(scan_data["warnings"]),
    )

    summary_table.add_row(
        "Critical",
        str(scan_data["critical"]),
    )

    layout["summary"].update(
        create_panel(
            summary_table,
            title="Scan Summary",
            border_style="cyan",
        )
    )

    # =========================
    # COST SUMMARY
    # =========================

    cost_data = {
        "EC2": 120,
        "S3": 35,
        "RDS": 60,
        "Lambda": 12,
    }

    layout["cost"].update(
        Panel(
            create_cost_table(cost_data),
            title="Estimated Monthly Cost",
            border_style="green",
        )
    )

    # =========================
    # COST OPTIMIZATION
    # =========================

    layout["optimization"].update(
        create_cost_optimization()
    )

    # =========================
    # RECOMMENDATIONS
    # =========================

    recommendation_text = Text()

    recommendation_text.append(
        "🔴 Critical\n",
        style="bold red",
    )

    recommendation_text.append(
        "• Enable CloudTrail Logging\n\n"
    )

    recommendation_text.append(
        "🟡 Warning\n",
        style="bold yellow",
    )

    recommendation_text.append(
        "• Remove Unused EBS Volumes\n\n"
    )

    recommendation_text.append(
        "🟢 Recommendation\n",
        style="bold green",
    )

    recommendation_text.append(
        "• Enable S3 Versioning\n"
    )

    recommendation_text.append(
        "• Reduce EC2 Idle Instances"
    )

    layout["right"].update(
        create_panel(
            recommendation_text,
            title="Recommendations",
            border_style="yellow",
        )
    )

    # =========================
    # FOOTER
    # =========================

    layout["footer"].update(
        create_panel(
            "Generated by Reporting Module",
            border_style="green",
        )
    )

    return layout