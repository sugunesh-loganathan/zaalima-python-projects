import typer

from app.utils import logger

app = typer.Typer()

@app.command()
def generate():
    """Generate infrastructure optimization reports."""
    logger.info("Generating report...")

    