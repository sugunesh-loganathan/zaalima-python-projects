from botocore.exceptions import ClientError

from aws.exceptions import AWSAuthenticationError
from utils.logger import logger


class AWSPaginator:
    """
    Reusable paginator for AWS service clients.
    """

    def __init__(self, client):
        self.client = client

    def paginate(self, operation_name, **kwargs):
        """
        Return all pages for a given AWS operation.
        """

        try:

            paginator = self.client.get_paginator(operation_name)

            pages = paginator.paginate(**kwargs)

            logger.info(f"Pagination successful for {operation_name}")

            return pages

        except ClientError as e:

            logger.error(f"Pagination failed: {e}")

            raise AWSAuthenticationError(str(e))