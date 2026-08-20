from rich.panel import Panel
from rich.table import Table


def create_cost_optimization():

    current_cost = 227
    potential_savings = 42
    optimized_cost = current_cost - potential_savings
    savings_percentage = (potential_savings / current_cost) * 100

    table = Table(show_header=False, expand=True)

    table.add_column("Metric", style="bold cyan")
    table.add_column("Value", justify="right")

    table.add_row(
        "Current Monthly Cost",
        f"${current_cost:.2f}",
    )

    table.add_row(
        "Potential Savings",
        f"${potential_savings:.2f}",
    )

    table.add_row(
        "Optimized Monthly Cost",
        f"${optimized_cost:.2f}",
    )

    table.add_row(
        "Savings Percentage",
        f"{savings_percentage:.1f}%",
    )

    return Panel(
        table,
        title="Cost Optimization",
        border_style="green",
    )