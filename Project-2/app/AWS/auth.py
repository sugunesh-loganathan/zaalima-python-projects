from app.utils import logger
import boto3
from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    ClientError,
)

from app.aws.session import AWSSession


class AWSAuthenticator:

    def __init__(self):
        self.session_manager = AWSSession()

    def authenticate(self):
        """
        Verify AWS credentials.
        """
        logger.info("Starting AWS authentication...")

        try:
            session = self.session_manager.create_session()

            sts = session.client("sts")

            identity = sts.get_caller_identity()

            logger.info("AWS credentials verified successfully.")

            return {
                "success": True,
                "account": identity["Account"],
                "user": identity["Arn"],
            }

        except NoCredentialsError:

            logger.error("AWS credentials not found.")

            return {
                "success": False,
                "message": "AWS credentials not found.",
            }

        except PartialCredentialsError:
                logger.error("Incomplete AWS credentials.")

                return {
                    "success": False,
                    "message": "Incomplete AWS credentials.",
                }

        except ClientError as e:
                logger.error(f"AWS Client Error: {e}")
                
                return {
                    "success": False,
                    "message": str(e),
                }

        except Exception as e:
                logger.error(f"Unexpected Error: {e}")

                return {
                    "success": False,
                    "message": str(e),
                }