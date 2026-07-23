import typer
from app.cli import (
    scan,
    report,
    cleanup,
    version,
)

from app.config import settings
from app.utils import logger

app = typer.Typer()

app.add_typer(scan.app, name="scan")
app.add_typer(report.app, name="report")
app.add_typer(cleanup.app, name="cleanup")
app.add_typer(version.app, name="version")


@app.command()
def scan():
    """Scan AWS infrastructure."""
    logger.info("Configuration Loaded Successfully")
    logger.info("Starting cloud infrastructure scan...")

if __name__ == "__main__":
    app()