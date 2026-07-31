"""
Report Generator Module

Generates the Rich terminal report.
"""

from rich.console import Console

from app.reporting.layout import create_layout

console = Console()


def generate_report():
    """
    Generate the cloud audit report.
    """

    try:
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

        layout = create_layout(scan_data)

        console.print(layout)

    except Exception as error:
        console.print(
            f"[bold red]Report generation failed:[/bold red] {error}"
        )