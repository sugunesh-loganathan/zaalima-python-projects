"""
Base scanner for all AWS resource scanners.
"""

import logging

import boto3
from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    NoCredentialsError,
    PartialCredentialsError,
)

from .exceptions import (
    AuthenticationError,
    PermissionError,
    RateLimitError,
    ResourceScanError,
)


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

    def handle_aws_error(self, error):
        """
        Convert AWS API errors into scanner-specific exceptions.
        """
        if isinstance(error, (NoCredentialsError, PartialCredentialsError)):
            raise AuthenticationError(
                "AWS credentials are missing or incomplete."
            ) from error

        if isinstance(error, ClientError):
            error_code = error.response.get(
                "Error", {}
            ).get("Code", "Unknown")

            if error_code in (
                "AccessDenied",
                "AccessDeniedException",
                "UnauthorizedOperation",
            ):
                raise PermissionError(
                    f"AWS permission denied: {error_code}"
                ) from error

            if error_code in (
                "Throttling",
                "ThrottlingException",
                "RequestLimitExceeded",
            ):
                raise RateLimitError(
                    f"AWS API rate limit exceeded: {error_code}"
                ) from error

            raise ResourceScanError(
                f"AWS API error: {error_code}"
            ) from error

        if isinstance(error, BotoCoreError):
            raise ResourceScanError(
                f"AWS SDK error: {error}"
            ) from error

        raise ResourceScanError(
            f"Unexpected scanner error: {error}"
        ) from error

    def scan(self):
        """
        Must be implemented by child scanner classes.
        """
        raise NotImplementedError(
            "Subclasses must implement scan()."
        )