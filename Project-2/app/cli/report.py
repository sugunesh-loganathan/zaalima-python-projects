import typer

from app.utils import logger
from app.reporting.report_generator import generate_report

app = typer.Typer()


@app.command()
def generate():
    """Generate infrastructure optimization reports."""

    logger.info("Generating report...")

    generate_report()