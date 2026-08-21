"""
Elastic IP Scanner Module
"""

from botocore.exceptions import BotoCoreError, ClientError

from .base import BaseScanner
from .exceptions import ScannerException


class ElasticIPScanner(BaseScanner):
    """Scanner for Elastic IP addresses."""

    def scan(self):
        """
        Scan Elastic IP addresses and return standardized results.
        """
        try:
            client = self.get_client("ec2")
            response = client.describe_addresses()

            results = []

            for address in response.get("Addresses", []):

                results.append({
                    "resource_type": "ElasticIP",
                    "resource_id": address.get("AllocationId"),
                    "status": (
                        "Associated"
                        if address.get("AssociationId")
                        else "Unassociated"
                    ),
                    "region": self.region_name,
                    "details": {
                        "public_ip": address.get("PublicIp"),
                        "instance_id": address.get("InstanceId"),
                        "network_interface_id": address.get("NetworkInterfaceId"),
                        "domain": address.get("Domain"),
                    },
                })

            self.logger.info("Elastic IP scan completed successfully.")
            return results

        except (ClientError, BotoCoreError) as error:
            self.logger.error(f"Elastic IP scan failed: {error}")
            raise ScannerException(str(error))