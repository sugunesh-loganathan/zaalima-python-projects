from rich.table import Table
from rich.panel import Panel


def create_report_statistics():

    table = Table(show_header=True, header_style="bold cyan", expand=True)

    table.add_column("Statistic")
    table.add_column("Value", justify="center")

    table.add_row("Scan Duration", "2.41 sec")
    table.add_row("Resources Scanned", "25")
    table.add_row("Reports Generated", "2")
    table.add_row("Cloud Provider", "AWS")

    return Panel(
        table,
        title="Report Statistics",
        border_style="bright_blue",
    )