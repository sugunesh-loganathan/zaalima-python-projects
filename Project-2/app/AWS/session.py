import boto3

from app.config import settings


class AWSSession:
    """
    Manages AWS boto3 sessions.
    """

    def create_session(self):
        """
        Create and return an AWS boto3 session.
        """

        return boto3.Session(
            region_name=settings.DEFAULT_REGION
        )

    def create_client(self, service_name):
        """
        Create an AWS service client using the configured session.
        """

        session = self.create_session()

        return session.client(service_name)