"""
Report Generator Module

Generates the Rich terminal report.
"""

import time

from rich.console import Console

from app.reporting.layout import create_layout
from app.reporting.logger import logger

console = Console()


def generate_report():
    """
    Generate the cloud audit report.
    """

    start_time = time.perf_counter()

    try:
        logger.info("Preparing scan data")

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

        required_keys = [
            "total_resources",
            "passed",
            "warnings",
            "critical",
            "recommendations",
        ]

        for key in required_keys:
            if key not in scan_data:
                raise ValueError(f"Missing required field: {key}")

        elapsed = time.perf_counter() - start_time
        scan_data["generation_time"] = round(elapsed, 4)

        logger.info("Generating dashboard")

        layout = create_layout(scan_data)

        console.print(layout)

        logger.info("Report generated successfully")

    except Exception as error:
        logger.exception("Report generation failed")

        console.print(
            f"[bold red]Report generation failed:[/bold red] {error}"
        )