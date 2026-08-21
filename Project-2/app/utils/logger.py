import logging

def setup_logger():

    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s | %(levelname)s | %(message)s",
    )

    return logging.getLogger("CloudAuditor")

logger = setup_logger()

