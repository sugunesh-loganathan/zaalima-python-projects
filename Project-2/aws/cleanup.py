from botocore.exceptions import ClientError

from aws.ebs import EBSService
from aws.eip import ElasticIPService
from aws.exceptions import AWSAuthenticationError
from utils.logger import logger
from aws.exceptions import AWSCleanupError

class CleanupService:
    """
    Service class for AWS cleanup operations.

    Supports:
    - Resource discovery
    - Resource validation
    - Dry-run cleanup
    - Safe cleanup helpers
    """

    def __init__(self, client_factory):

        self.client_factory = client_factory

        self.ebs_service = EBSService(client_factory)
        self.eip_service = ElasticIPService(client_factory)

        self.ec2_client = client_factory.get_client("ec2")

    # --------------------------------------------------
    # EBS
    # --------------------------------------------------

    def get_unused_volumes(self):
        """
        Return EBS volumes eligible for cleanup.
        """

        volumes = self.ebs_service.list_volumes()

        return [
            volume
            for volume in volumes
            if self.validate_volume(volume)
        ]

    def validate_volume(self, volume):
        """
        Validate whether an EBS volume is eligible
        for cleanup.
        """

        return (
            volume.get("State") == "available"
            and volume.get("Attachments", 0) == 0
        )

    # --------------------------------------------------
    # Elastic IP
    # --------------------------------------------------

    def get_unused_elastic_ips(self):
        """
        Return Elastic IPs eligible for cleanup.
        """

        addresses = self.eip_service.list_addresses()

        return [
            address
            for address in addresses
            if self.validate_elastic_ip(address)
        ]

    def validate_elastic_ip(self, address):
        """
        Validate whether an Elastic IP is unassociated.
        """

        return address.get("InstanceId") is None

    # --------------------------------------------------
    # EC2
    # --------------------------------------------------

    def validate_instance(self, instance):
        """
        Validate EC2 instance information.

        No instance is terminated here.
        """

        instance_id = instance.get("InstanceId")
        state = instance.get("State")

        return (
            instance_id is not None
            and state is not None
        )

    # --------------------------------------------------
    # EBS CLEANUP HELPER
    # --------------------------------------------------

    def cleanup_volume(self, volume_id, dry_run=True):
        """
        Delete an EBS volume or preview the deletion.
        """

        if not volume_id:
            raise ValueError("Volume ID is required.")

        if dry_run:

            logger.info(
                f"[DRY RUN] EBS volume {volume_id} would be deleted."
            )

            return {
                "resource_type": "EBS",
                "resource_id": volume_id,
                "action": "delete",
                "dry_run": True,
                "status": "preview"
            }

        try:

            self.ec2_client.delete_volume(
                VolumeId=volume_id
            )

            logger.info(
                f"EBS volume {volume_id} deleted successfully."
            )

            return {
                "resource_type": "EBS",
                "resource_id": volume_id,
                "action": "delete",
                "dry_run": False,
                "status": "deleted"
            }

        except ClientError as e:

            error_code = e.response["Error"]["Code"]

            logger.error(
                f"Failed to delete EBS volume "
                f"{volume_id} | Error: {error_code}"
            )

            raise AWSCleanupError(
                f"Failed to delete EBS volume "
                f"{volume_id}: {error_code}"
            )

    def cleanup_elastic_ip(self, allocation_id, dry_run=True):
        """
        Release an Elastic IP or preview the release.
        """

        if not allocation_id:
            raise ValueError("Allocation ID is required.")

        if dry_run:

            logger.info(
                f"[DRY RUN] Elastic IP {allocation_id} "
                f"would be released."
            )

            return {
                "resource_type": "Elastic IP",
                "resource_id": allocation_id,
                "action": "release",
                "dry_run": True,
                "status": "preview"
            }

        try:

            self.ec2_client.release_address(
                AllocationId=allocation_id
            )

            logger.info(
                f"Elastic IP {allocation_id} "
                f"released successfully."
            )

            return {
                "resource_type": "Elastic IP",
                "resource_id": allocation_id,
                "action": "release",
                "dry_run": False,
                "status": "released"
            }

        except ClientError as e:

            error_code = e.response["Error"]["Code"]

            logger.error(
                f"Failed to release Elastic IP "
                f"{allocation_id} | Error: {error_code}"
            )

            raise AWSCleanupError(
                f"Failed to release Elastic IP "
                f"{allocation_id}: {error_code}"
            )

    def dry_run(self):
        """
        Preview all cleanup candidates.

        No AWS resources are modified.
        """

        unused_volumes = self.get_unused_volumes()
        unused_eips = self.get_unused_elastic_ips()

        print("\n" + "=" * 60)
        print("CLEANUP DRY RUN")
        print("=" * 60)

        volume_results = []

        print("\nEBS Volumes eligible for cleanup:")

        if unused_volumes:

            for volume in unused_volumes:

                result = self.cleanup_volume(
                    volume["VolumeId"],
                    dry_run=True
                )

                volume_results.append(result)

                print(
                    f"  - {volume['VolumeId']} "
                    f"would be deleted."
                )

        else:

            print(
                "  No EBS volumes eligible for cleanup."
            )

        eip_results = []

        print("\nElastic IPs eligible for cleanup:")

        if unused_eips:

            for address in unused_eips:

                result = self.cleanup_elastic_ip(
                    address["AllocationId"],
                    dry_run=True
                )

                eip_results.append(result)

                print(
                    f"  - {address['PublicIp']} "
                    f"would be released."
                )

        else:

            print(
                "  No Elastic IPs eligible for cleanup."
            )

        print("\n" + "-" * 60)
        print("DRY RUN ONLY")
        print("No AWS resources were modified.")
        print("-" * 60)

        return {
            "volumes": volume_results,
            "elastic_ips": eip_results
        }