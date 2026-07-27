import boto3

from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    ClientError,
    ProfileNotFound
)

from config.config import Config
from utils.logger import logger
from aws.exceptions import AWSAuthenticationError


class AWSAuth:
    """
    Handles AWS authentication and session management.
    """

    def __init__(self, profile_name=None, region_name=None):
        self.profile_name = profile_name
        self.config = Config(region_name)
        self.session = None

    def create_session(self):
        """
        Create and return a boto3 session.
        Reuses the existing session if already created.
        """

        # Reuse existing session
        if self.session is not None:
            logger.info("Using existing AWS session.")
            return self.session

        try:
            # Validate region before creating session
            self.config.validate_region()

            self.session = boto3.Session(
                profile_name=self.profile_name,
                region_name=self.config.get_region()
            )

            logger.info(
                f"AWS Session created successfully "
                f"(Region: {self.config.get_region()}, "
                f"Profile: {self.profile_name or 'default'})"
            )

            return self.session

        except ProfileNotFound:
            logger.error("AWS profile not found.")
            raise AWSAuthenticationError("AWS profile not found.")

        except Exception as e:
            logger.error(f"Failed to create AWS session: {e}")
            raise AWSAuthenticationError(str(e))

    def validate_credentials(self):
        """
        Validate AWS credentials using STS.
        """

        try:

            if self.session is None:
                self.create_session()

            sts = self.session.client("sts")

            identity = sts.get_caller_identity()

            logger.info("AWS credentials validated successfully.")

            return identity

        except NoCredentialsError:
            logger.error("AWS credentials not found.")
            raise AWSAuthenticationError("AWS credentials not found.")

        except PartialCredentialsError:
            logger.error("Incomplete AWS credentials.")
            raise AWSAuthenticationError("Incomplete AWS credentials.")

        except ProfileNotFound:
            logger.error("AWS profile not found.")
            raise AWSAuthenticationError("AWS profile not found.")

        except ClientError as e:
            logger.error(f"AWS Client Error: {e}")
            raise AWSAuthenticationError(str(e))

        except Exception as e:
            logger.error(f"Unexpected authentication error: {e}")
            raise AWSAuthenticationError(str(e))