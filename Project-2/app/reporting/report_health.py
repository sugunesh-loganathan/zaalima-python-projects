from rich.panel import Panel
from rich.text import Text


def create_report_health(scan_data):

    if scan_data["critical"] > 0:
        text = Text("🔴 Critical Environment", style="bold red")

    elif scan_data["warnings"] > 0:
        text = Text("🟡 Needs Attention", style="bold yellow")

    else:
        text = Text("🟢 Healthy", style="bold green")

    return Panel(
        text,
        title="Environment Health",
        border_style="red",
    )