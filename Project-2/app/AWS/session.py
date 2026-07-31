import boto3

from app.config import settings


class AWSSession:

    def create_session(self):

        return boto3.Session(
            region_name=settings.DEFAULT_REGION
        )