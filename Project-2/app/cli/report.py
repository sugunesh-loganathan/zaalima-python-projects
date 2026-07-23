import typer

from app.utils import logger

app = typer.Typer()

@app.command()
def generate():
    """Generate infrastructure report."""
    logger.info("Generating report...")

    