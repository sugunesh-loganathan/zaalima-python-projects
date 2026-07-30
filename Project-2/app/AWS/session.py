import boto3


class AWSSession:

    def create_session(self):
        """
        Create a boto3 session.
        """

        return boto3.Session()