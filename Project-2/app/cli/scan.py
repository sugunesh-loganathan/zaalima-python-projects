import typer

from app.utils import logger

app = typer.Typer()

@app.command()
def run():
    """Scan AWS Infrastructure"""
    logger.info("Starting infrastructure scan...")

    