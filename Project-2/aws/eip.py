from botocore.exceptions import ClientError

from aws.client_factory import AWSClientFactory
from aws.exceptions import AWSAuthenticationError
from aws.pagination import AWSPaginator
from utils.logger import logger
from utils.retry import aws_retry


class ElasticIPService:
    """
    Service class for AWS Elastic IP operations.
    """

    def __init__(self, client_factory: AWSClientFactory):
        self.client = client_factory.get_client("ec2")

    def get_addresses(self):
        """
        Fetch all Elastic IPs.
        """
        try:

            response = self.client.describe_addresses()

            logger.info("Elastic IPs fetched successfully.")

            return response

        except ClientError as e:

            logger.error(f"Failed to fetch Elastic IPs: {e}")

            raise AWSAuthenticationError(str(e))

    def list_addresses(self):
        """
        Return simplified Elastic IP details.
        """
        addresses = []

        response = self.get_addresses()

        for address in response["Addresses"]:
            addresses.append({
                "AllocationId": address.get("AllocationId"),
                "PublicIp": address.get("PublicIp"),
                "PrivateIp": address.get("PrivateIpAddress"),
                "InstanceId": address.get("InstanceId"),
                "AssociationId": address.get("AssociationId"),
                "Domain": address.get("Domain")
            })

        return addresses

    def get_unassociated_addresses(self, addresses=None):
        """
        Return Elastic IPs not associated with any EC2 instance.
        """
        if addresses is None:
            addresses = self.list_addresses()

        return [
            address
            for address in addresses
            if address["InstanceId"] is None
        ]

    