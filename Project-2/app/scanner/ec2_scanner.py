"""
EC2 Scanner Module
"""

from botocore.exceptions import BotoCoreError, ClientError

from .base import BaseScanner
from .exceptions import ScannerException


class EC2Scanner(BaseScanner):
    """Scanner for EC2 resources."""

    def scan(self):
        """
        Scan EC2 instances and return standardized results.
        """
        try:
            client = self.get_client("ec2")
            response = client.describe_instances()

            results = []

            for reservation in response.get("Reservations", []):
                for instance in reservation.get("Instances", []):

                    results.append({
                        "resource_type": "EC2",
                        "resource_id": instance.get("InstanceId"),
                        "status": instance.get("State", {}).get("Name"),
                        "region": self.region_name,
                        "details": {
                            "instance_type": instance.get("InstanceType"),
                            "public_ip": instance.get("PublicIpAddress"),
                            "private_ip": instance.get("PrivateIpAddress")
                        }
                    })

            self.logger.info("EC2 scan completed successfully.")
            return results

        except (ClientError, BotoCoreError) as error:
            self.logger.error(f"EC2 scan failed: {error}")
            raise ScannerException(str(error))