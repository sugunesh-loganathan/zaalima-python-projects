"""
Report Generator Module

This module prepares the scan data and generates
the final Rich terminal report.
"""

from rich.console import Console
from app.reporting.layout import create_layout

console = Console()


def generate_report():
    """
    Generate the terminal report.

    This function prepares sample scan data,
    creates the dashboard layout and prints
    the report to the terminal.
    """

    scan_data = {
        "total_resources": 25,
        "passed": 18,
        "warnings": 5,
        "critical": 2,
        "recommendations": [
            "Enable S3 Versioning",
            "Remove Unused EBS Volumes",
            "Enable CloudTrail Logging",
            "Reduce EC2 Idle Instances",
        ],
    }

    layout = create_layout(scan_data)

    console.print(layout)