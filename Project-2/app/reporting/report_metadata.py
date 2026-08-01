from datetime import datetime
from rich.table import Table

from app.reporting.config import (
    REPORT_ID,
    CLOUD_PROVIDER,
    AUDITOR,
    SECURITY_SCORE,
)


def create_metadata_table():
    table = Table(show_header=False, expand=True)

    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    table.add_row("Report ID", REPORT_ID)
    table.add_row("Generated", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    table.add_row("Cloud Provider", CLOUD_PROVIDER)
    table.add_row("Auditor", AUDITOR)
    table.add_row("Security Score", f"{SECURITY_SCORE}%")

    return table