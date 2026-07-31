from botocore.exceptions import ClientError

from aws.client_factory import AWSClientFactory
from aws.exceptions import AWSAuthenticationError
from utils.logger import logger

class EBSService:

    def __init__(self, client_factory: AWSClientFactory):
        self.client = client_factory.get_client("ec2")

    def get_volumes(self):

        try:

            response = self.client.describe_volumes()

            logger.info("EBS volumes fetched successfully.")

            return response

        except ClientError as e:

            logger.error(f"Failed to fetch EBS volumes: {e}")

            raise AWSAuthenticationError(str(e))

    def list_volumes(self):

        volumes = []

        response = self.get_volumes()

        for volume in response["Volumes"]:

            volumes.append({

                "VolumeId": volume["VolumeId"],

                "Size": volume["Size"],

                "State": volume["State"],

                "VolumeType": volume["VolumeType"],

                "AvailabilityZone": volume["AvailabilityZone"],

                "Encrypted": volume["Encrypted"],

                "Attachments": len(volume["Attachments"])

            })

        return volumes
    
    def get_unattached_volumes(self, volumes=None):

        if volumes is None:
            volumes = self.list_volumes()

        return [
            volume
            for volume in volumes
            if volume["Attachments"] == 0
        ]