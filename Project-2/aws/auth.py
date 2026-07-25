import boto3
from config.config import Config

from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    ClientError,
    ProfileNotFound
)

from aws.exceptions import AWSAuthenticationError

#create awsauth class
class AWSAuth:

    def __init__(self, profile_name=None, region_name=None):

        self.profile_name = profile_name

        self.config = Config(region_name)

        self.session = None

#Create Session Method
    def create_session(self):

        self.config.validate_region()

        self.session = boto3.Session(
            profile_name=self.profile_name,
            region_name=self.config.get_region()
    )

        return self.session
#validation and error handling
    def validate_credentials(self):

        try:

            if self.session is None:
                self.create_session()

            sts = self.session.client("sts")

            return sts.get_caller_identity()

        except (
            NoCredentialsError,
            PartialCredentialsError,
            ProfileNotFound,
            ClientError
        ) as e:

            raise AWSAuthenticationError(str(e))