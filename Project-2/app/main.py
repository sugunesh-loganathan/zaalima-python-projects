import typer

from app.config import settings
from app.utils import logger

app = typer.Typer()


@app.command()
def scan():
    """Scan AWS infrastructure."""
    logger.info("Configuration Loaded Successfully")
    logger.info("Starting cloud infrastructure scan...")

if __name__ == "__main__":
    app()