import typer

from app.utils import logger

app = typer.Typer()

@app.command()
def run():
    """Cleanup unused resources."""
    logger.info("Running cleanup...")