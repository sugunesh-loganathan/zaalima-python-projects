from rich.panel import Panel
from rich.table import Table


def create_report_version():

    table = Table(show_header=False, expand=True)

    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    table.add_row("Module Version", "1.2.0")
    table.add_row("Template Version", "v2")
    table.add_row("Report Format", "Rich CLI")

    return Panel(
        table,
        title="Version Information",
        border_style="bright_blue",
    )