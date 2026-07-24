from botocore.exceptions import ClientError

from aws.auth import AWSAuth
from aws.exceptions import AWSAuthenticationError

class AWSClientFactory:

    def __init__(self, auth: AWSAuth):
        self.auth = auth

    def get_session(self):

        if self.auth.session is None:
            self.auth.create_session()

        return self.auth.session

    def get_client(self, service_name):

        try:

            session = self.get_session()

            return session.client(service_name)

        except ClientError as e:

            raise AWSAuthenticationError(str(e))