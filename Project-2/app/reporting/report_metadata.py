from rich.table import Table
from datetime import datetime


def create_metadata_table():
    table = Table(show_header=False, expand=True)

    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    table.add_row("Report ID", "REP-2026-001")
    table.add_row("Generated", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    table.add_row("Cloud Provider", "AWS")
    table.add_row("Auditor", "Sreejani")
    table.add_row("Security Score", "92%")

    return table