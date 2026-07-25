import typer

from app.utils import logger

app = typer.Typer()

@app.command()
def run():
    """Scan AWS cloud infrastructure for unused and underutilized resources."""
    logger.info("Starting infrastructure scan...")

    