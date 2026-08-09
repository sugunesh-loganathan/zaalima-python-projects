from aws.ebs import EBSService
from aws.eip import ElasticIPService


class CleanupService:
    """
    Service class for AWS cleanup operations.

    This module identifies and validates resources
    that may be eligible for cleanup.

    Actual deletion/release operations are not performed
    during dry-run mode.
    """

    def __init__(self, client_factory):
        self.ebs_service = EBSService(client_factory)
        self.eip_service = ElasticIPService(client_factory)

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

        This method does not terminate the instance.
        """

        instance_id = instance.get("InstanceId")
        state = instance.get("State")

        return (
            instance_id is not None
            and state is not None
        )

    # --------------------------------------------------
    # DRY RUN
    # --------------------------------------------------

    def dry_run(self):
        """
        Preview resources that are eligible for cleanup.

        No AWS resources are deleted or released.
        """

        unused_volumes = self.get_unused_volumes()
        unused_eips = self.get_unused_elastic_ips()

        print("\n" + "=" * 60)
        print("CLEANUP DRY RUN")
        print("=" * 60)

        print("\nEBS Volumes eligible for cleanup:")

        if unused_volumes:

            for volume in unused_volumes:
                print(
                    f"  - {volume['VolumeId']} | "
                    f"State: {volume['State']} | "
                    f"Attachments: {volume['Attachments']}"
                )

        else:
            print("  No EBS volumes eligible for cleanup.")

        print("\nElastic IPs eligible for cleanup:")

        if unused_eips:

            for address in unused_eips:
                print(
                    f"  - {address['PublicIp']} | "
                    f"InstanceId: {address['InstanceId']}"
                )

        else:
            print("  No Elastic IPs eligible for cleanup.")

        print("\n" + "-" * 60)
        print("DRY RUN ONLY")
        print("No AWS resources were deleted or released.")
        print("-" * 60)

        return {
            "volumes": unused_volumes,
            "elastic_ips": unused_eips
        }