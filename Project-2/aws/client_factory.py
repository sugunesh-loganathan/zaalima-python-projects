from botocore.exceptions import ClientError

from aws.auth import AWSAuth
from aws.exceptions import AWSAuthenticationError
from utils.logger import logger


class AWSClientFactory:
    """
    Creates reusable AWS service clients.
    """

    SUPPORTED_SERVICES = {
        "ec2",
        "sts",
        "cloudwatch",
        "s3"
    }

    def __init__(self, auth: AWSAuth):
        self.auth = auth

    def get_session(self):
        """
        Return existing session or create one.
        """
        return self.auth.create_session()

    def get_client(self, service_name: str):
        """
        Return boto3 client for a supported AWS service.
        """

        if service_name not in self.SUPPORTED_SERVICES:
            raise ValueError(f"Unsupported AWS service: {service_name}")

        try:
            session = self.get_session()

            client = session.client(service_name)

            logger.info(f"{service_name} client created successfully.")

            return client

        except ClientError as e:
            logger.error(e)
            raise AWSAuthenticationError(str(e))