import typer
from app.cli import (
    scan,
    report,
    cleanup,
    version,
)

from app.config import settings
from app.utils import logger

app = typer.Typer(
    help="Cloud Infrastructure Auditor & Cost Optimizer CLI"
)

app.add_typer(scan.app, name="scan")
app.add_typer(report.app, name="report")
app.add_typer(cleanup.app, name="cleanup")
app.add_typer(version.app, name="version")



if __name__ == "__main__":
    app()
