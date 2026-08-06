import typer

from app.utils import logger
from app.scanner.scanner_manager import ScannerManager

app = typer.Typer()


@app.command()
def run():
    """
    Scan AWS cloud infrastructure for unused and underutilized resources.
    """

    logger.info("Starting infrastructure scan...")

    manager = ScannerManager()

    results = manager.scan_all()

    for result in results:

        logger.info(f"Service          : {result['service']}")
        logger.info(f"Status           : {result['status']}")
        logger.info(f"Resources Found  : {result['resources_found']}")
        logger.info(f"Message          : {result['message']}")

        if "instances" in result:
            for instance in result["instances"]:
                logger.info(
                    f"Instance: {instance['instance_id']} | "
                    f"State: {instance['state']} | "
                    f"Type: {instance['type']}"
                )

    logger.info("Infrastructure scan completed.")