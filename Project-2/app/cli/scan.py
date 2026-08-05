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

    result = scanner.scan()

    logger.info(f"Service          : {result['service']}")
    logger.info(f"Status           : {result['status']}")
    logger.info(f"Resources Found  : {result['resources_found']}")
    logger.info(f"Message          : {result['message']}")

    for instance in result["instances"]:
        logger.info(
            f"Instance: {instance['instance_id']} | "
            f"State: {instance['state']} | "
            f"Type: {instance['type']}"
        )

    logger.info("Infrastructure scan completed.")