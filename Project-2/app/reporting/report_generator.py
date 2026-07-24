from rich.console import Console
from app.reporting.layout import create_layout

console = Console()


def generate_report():
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