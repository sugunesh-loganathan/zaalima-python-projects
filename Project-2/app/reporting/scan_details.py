from datetime import datetime

from rich.panel import Panel
from rich.table import Table


def create_scan_details(scan_data):
    table = Table(show_header=False, expand=True)

    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    table.add_row(
        "Scan Started",
        datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    )

    table.add_row(
        "Status",
        "Completed",
    )

    table.add_row(
        "Duration",
        f"{scan_data.get('generation_time', 0.0):.4f} sec",
    )

    return Panel(
        table,
        title="Scan Details",
        border_style="blue",
    )