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
        Simulate scanning EC2 instances.
        """

        instances = [
            {
                "instance_id": "i-01abc123",
                "state": "stopped",
                "type": "t2.micro",
                "cpu_utilization": 2,
            },
            {
                "instance_id": "i-02def456",
                "state": "running",
                "type": "t3.small",
                "cpu_utilization": 48,
            },
        ]

        # Analyze each instance
        for instance in instances:

            if instance["state"] == "stopped":
                instance["recommendation"] = "Safe to terminate"

            elif instance["cpu_utilization"] < 10:
                instance["recommendation"] = "Underutilized"

            else:
                instance["recommendation"] = "Healthy"

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