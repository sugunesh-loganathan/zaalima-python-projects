from rich.panel import Panel
from rich.text import Text


def create_audit_status(scan_data):

    if scan_data["critical"] == 0:
        status = Text("✔ PASSED", style="bold green")

    elif scan_data["critical"] <= 2:
        status = Text("⚠ REVIEW REQUIRED", style="bold yellow")

    else:
        status = Text("✖ FAILED", style="bold red")

    return Panel(
        status,
        title="Audit Result",
        border_style="bright_blue",
    )