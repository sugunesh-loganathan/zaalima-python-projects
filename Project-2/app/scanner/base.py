"""
Base scanner for all AWS resource scanners.
"""

import logging

import boto3


class BaseScanner:
    """Base class for all AWS resource scanners."""

    def __init__(self, region_name="us-east-1"):
        """
        Initialize AWS session and logger.
        """
        self.region_name = region_name
        self.session = boto3.Session(region_name=region_name)

        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    def get_client(self, service_name):
        """
        Return a boto3 client for the requested AWS service.
        """
        return self.session.client(service_name)

    def create_result(
        self,
        resource_type,
        resource_id,
        status,
        details=None
    ):
        """
        Create a standardized scanner result.
        """
        return {
            "resource_type": resource_type,
            "resource_id": resource_id,
            "status": status,
            "region": self.region_name,
            "details": details or {},
        }

    def scan(self):
        """
        Must be implemented by child scanner classes.
        """
        raise NotImplementedError("Subclasses must implement scan().")