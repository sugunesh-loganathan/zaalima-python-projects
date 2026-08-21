from botocore.exceptions import ClientError

from aws.client_factory import AWSClientFactory
from aws.exceptions import AWSAuthenticationError
from aws.pagination import AWSPaginator
from utils.logger import logger
from utils.retry import aws_retry

class EBSService:
    """
    Service class for AWS EBS volume operations.
    """

    def __init__(self, client_factory: AWSClientFactory):
        self.client = client_factory.get_client("ec2")
        
    @aws_retry()

    def get_volumes(self):
        """
        Fetch all EBS volumes using pagination.
        """
        try:
            paginator = AWSPaginator(self.client)

            pages = paginator.paginate("describe_volumes")

            volumes = []

            for page in pages:
                volumes.extend(page["Volumes"])

            logger.info("EBS volumes fetched successfully.")

            return {"Volumes": volumes}

        except ClientError as e:
            logger.error(f"Failed to fetch EBS volumes: {e}")
            raise AWSAuthenticationError(str(e))

    def list_volumes(self):
        """
        Return simplified EBS volume details.
        """
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
        """
        Return all unattached EBS volumes.
        """
        if volumes is None:
            volumes = self.list_volumes()

        return [
            volume
            for volume in volumes
            if volume["Attachments"] == 0
        ]