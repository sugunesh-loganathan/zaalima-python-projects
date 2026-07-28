from rich.table import Table
from rich.panel import Panel


def create_resource_summary(resource_data):

    table = Table(show_header=True, header_style="bold cyan", expand=True)

    table.add_column("Service")
    table.add_column("Resources", justify="center")

    total = 0

    for service, count in resource_data.items():
        table.add_row(service, str(count))
        total += count

    table.add_row("[bold]TOTAL[/bold]", f"[bold]{total}[/bold]")

    return Panel(
        table,
        title="Resource Summary",
        border_style="blue",
    )