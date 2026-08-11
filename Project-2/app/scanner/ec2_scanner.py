from app.scanner.base_scanner import BaseScanner
from app.models.scan_result import ScanResult
from app.aws.session import AWSSession


class EC2Scanner(BaseScanner):
    """
    Scanner for EC2 resources.
    """

    def __init__(self):
        self.session_manager = AWSSession()

    def get_client(self):
        """
        Create and return an EC2 boto3 client.
        """

        return self.session_manager.create_client("ec2")

    def scan(self):
        """
        Discover and analyze EC2 instances.
        """

        ec2 = self.get_client()

        response = ec2.describe_instances()

        instances = []

        for reservation in response["Reservations"]:

            for instance in reservation["Instances"]:

                instance_data = {
                    "instance_id": instance["InstanceId"],
                    "state": instance["State"]["Name"],
                    "type": instance["InstanceType"],
                }

                instances.append(instance_data)

        # Analyze each instance
        for instance in instances:

            if instance["state"] == "stopped":
                instance["recommendation"] = "Safe to terminate"

            elif instance["state"] == "running":
                instance["recommendation"] = "Healthy"

            else:
                instance["recommendation"] = "Review required"

        result = ScanResult(
            service="EC2",
            status="success",
            resources_found=len(instances),
            message="EC2 scan completed successfully.",
        )

        return {
            **result.to_dict(),
            "instances": instances,
        }