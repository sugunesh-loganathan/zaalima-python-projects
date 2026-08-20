import typer

from app.utils import logger

app = typer.Typer()

@app.command()
def run():
    """Remove unused cloud resources after user confirmation."""
    logger.info("Running cleanup...")