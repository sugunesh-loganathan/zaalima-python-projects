"""
EBS Scanner Module
"""

from botocore.exceptions import BotoCoreError, ClientError

from .base import BaseScanner
from .exceptions import ScannerException


class EBSScanner(BaseScanner):
    """Scanner for EBS volumes."""

    def scan(self):
        """
        Scan EBS volumes and return standardized results.
        """
        try:
            client = self.get_client("ec2")
            response = client.describe_volumes()

            results = []

            for volume in response.get("Volumes", []):

                attachments = volume.get("Attachments", [])

                results.append({
                    "resource_type": "EBS",
                    "resource_id": volume.get("VolumeId"),
                    "status": volume.get("State"),
                    "region": self.region_name,
                    "details": {
                        "size_gb": volume.get("Size"),
                        "volume_type": volume.get("VolumeType"),
                        "encrypted": volume.get("Encrypted"),
                        "attached": len(attachments) > 0,
                        "instance_id": (
                            attachments[0].get("InstanceId")
                            if attachments else None
                        )
                    }
                })

            self.logger.info("EBS scan completed successfully.")
            return results

        except (ClientError, BotoCoreError) as error:
            self.logger.error(f"EBS scan failed: {error}")
            raise ScannerException(str(error))
