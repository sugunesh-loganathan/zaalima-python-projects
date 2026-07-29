import boto3

class AWSSession:

    def create_session(self):
        return boto3.Session()
            