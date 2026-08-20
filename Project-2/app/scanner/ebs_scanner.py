from app.scanner.base_scanner import BaseScanner
from app.models.scan_result import ScanResult
from app.aws.session import AWSSession

from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    ClientError,
)

from app.utils import logger


class EBSScanner(BaseScanner):
    """
    Scanner for EBS volumes.
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
        Discover and analyze EBS volumes.
        """

        logger.info("Starting EBS volume scan...")

        try:
            ec2 = self.get_client()

            response = ec2.describe_volumes()

            volumes = []

            for volume in response.get("Volumes", []):

                attachments = volume.get("Attachments", [])

                volume_data = {
                    "volume_id": volume.get("VolumeId"),
                    "state": volume.get("State"),
                    "size_gb": volume.get("Size"),
                    "volume_type": volume.get("VolumeType"),
                    "encrypted": volume.get("Encrypted"),
                    "instance_id": (
                        attachments[0].get("InstanceId")
                        if attachments else None
                    ),
                }

                # Analyze the volume
                if volume_data["state"] == "available":
                    volume_data["recommendation"] = (
                        "Unused volume - review for deletion"
                    )
                else:
                    volume_data["recommendation"] = "In use"

                volumes.append(volume_data)

            logger.info(
                f"EBS scan completed. Resources found: {len(volumes)}"
            )

            result = ScanResult(
                service="EBS",
                status="success",
                resources_found=len(volumes),
                message="EBS scan completed successfully.",
            )

            return {
                **result.to_dict(),
                "volumes": volumes,
            }

        except NoCredentialsError:

            logger.error("AWS credentials not found.")

            result = ScanResult(
                service="EBS",
                status="failed",
                resources_found=0,
                message="AWS credentials not found.",
            )

            return result.to_dict()

        except PartialCredentialsError:

            logger.error("Incomplete AWS credentials.")

            result = ScanResult(
                service="EBS",
                status="failed",
                resources_found=0,
                message="Incomplete AWS credentials.",
            )

            return result.to_dict()

        except ClientError as e:

            logger.error(f"AWS EBS API error: {e}")

            result = ScanResult(
                service="EBS",
                status="failed",
                resources_found=0,
                message=f"AWS EBS API error: {e}",
            )

            return result.to_dict()

        except Exception as e:

            logger.error(f"Unexpected EBS scanner error: {e}")

            result = ScanResult(
                service="EBS",
                status="failed",
                resources_found=0,
                message=f"Unexpected scanner error: {e}",
            )

            return result.to_dict()