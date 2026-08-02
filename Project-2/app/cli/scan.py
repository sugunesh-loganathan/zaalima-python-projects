import typer

from app.utils import logger
from app.scanner.ec2_scanner import EC2Scanner

app = typer.Typer()

@app.command()
def run():
    """
    Scan AWS cloud infrastructure for unused and underutilized resources.
    """

    logger.info("Starting infrastructure scan...")

    scanner = EC2Scanner()

    scanner.scan()

    logger.info("Infrastructure scan completed.")