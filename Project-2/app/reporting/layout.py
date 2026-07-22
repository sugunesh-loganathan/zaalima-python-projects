from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def display_report():
    # Report Header
    console.print(
        Panel.fit(
            "[bold cyan]Cloud Infrastructure Auditor & Cost Optimizer[/bold cyan]",
            title="Project 2",
            border_style="green",
        )
    )

    # Scan Summary Table
    table = Table(title="Scan Summary")

    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="center", style="magenta")

    table.add_row("Total Resources", "25")
    table.add_row("Passed Checks", "21")
    table.add_row("Warnings", "3")
    table.add_row("Critical Issues", "1")

    console.print(table)


if __name__ == "__main__":
    display_report()