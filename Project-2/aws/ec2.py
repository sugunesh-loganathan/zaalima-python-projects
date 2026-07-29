from botocore.exceptions import ClientError

from aws.client_factory import AWSClientFactory
from aws.exceptions import AWSAuthenticationError
from utils.logger import logger


class EC2Service:

    def __init__(self, client_factory):
        self.client = client_factory.get_client("ec2")

    def get_instances(self):

        try:

            response = self.client.describe_instances()

            logger.info("EC2 instances fetched successfully.")

            return response

        except ClientError as e:

            logger.error(e)

            raise AWSAuthenticationError(str(e))

    def list_instances(self):

        instances = []

        response = self.get_instances()

        for reservation in response["Reservations"]:

            for instance in reservation["Instances"]:

                instances.append({

                    "InstanceId": instance["InstanceId"],

                    "InstanceType": instance["InstanceType"],

                    "State": instance["State"]["Name"],

                    "AvailabilityZone":
                    instance["Placement"]["AvailabilityZone"],

                    "PrivateIP":
                    instance.get("PrivateIpAddress"),

                    "PublicIP":
                    instance.get("PublicIpAddress")

                })

        return instances