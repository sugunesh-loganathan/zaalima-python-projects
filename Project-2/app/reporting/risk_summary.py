from rich.panel import Panel
from rich.table import Table


def create_risk_summary(scan_data):

    table = Table(show_header=True, header_style="bold white", expand=True)

    table.add_column("Risk Level")
    table.add_column("Resources", justify="center")

    table.add_row(
        "[red]Critical[/red]",
        str(scan_data["critical"])
    )

    table.add_row(
        "[yellow]Warning[/yellow]",
        str(scan_data["warnings"])
    )

    table.add_row(
        "[green]Passed[/green]",
        str(scan_data["passed"])
    )

    return Panel(
        table,
        title="Risk Summary",
        border_style="red",
    )