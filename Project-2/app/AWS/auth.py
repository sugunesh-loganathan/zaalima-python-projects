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

        try:
            session = self.session_manager.create_session()

            sts = session.client("sts")

            identity = sts.get_caller_identity()

            return {
                "success": True,
                "account": identity["Account"],
                "user": identity["Arn"],
            }

        except NoCredentialsError:
            return {
                "success": False,
                "message": "AWS credentials not found.",
            }

        except PartialCredentialsError:
            return {
                "success": False,
                "message": "Incomplete AWS credentials.",
            }

        except ClientError as e:
            return {
                "success": False,
                "message": str(e),
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e),
            }