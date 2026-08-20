import platform

from rich.panel import Panel
from rich.table import Table


def create_system_information():

    table = Table(show_header=False, expand=True)

    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    table.add_row("Operating System", platform.system())
    table.add_row(
        "Python Version",
        platform.python_version(),
    )
    table.add_row("Report Mode", "Development")

    return Panel(
        table,
        title="System Information",
        border_style="bright_magenta",
    )