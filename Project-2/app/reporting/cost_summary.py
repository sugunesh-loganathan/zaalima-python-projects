from rich.table import Table


def create_cost_table(cost_data):
    table = Table(show_header=True, header_style="bold green")

    table.add_column("Service")
    table.add_column("Monthly Cost ($)", justify="right")

    total = 0

    for service, cost in cost_data.items():
        table.add_row(service, f"${cost}")
        total += cost

    table.add_section()
    table.add_row("TOTAL", f"${total}")

    return table