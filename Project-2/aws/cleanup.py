from aws.ebs import EBSService
from aws.eip import ElasticIPService


class CleanupService:
    """
    Service class for AWS cleanup operations.

    This module only identifies and validates resources
    that may be eligible for cleanup.

    No AWS resources are deleted or released here.
    """

    def __init__(self, client_factory):
        self.ebs_service = EBSService(client_factory)
        self.eip_service = ElasticIPService(client_factory)

    # --------------------------------------------------
    # EBS
    # --------------------------------------------------

    def get_unused_volumes(self):
        """
        Return EBS volumes that are potentially unused.
        """
        volumes = self.ebs_service.list_volumes()

        return [
            volume
            for volume in volumes
            if self.validate_volume(volume)
        ]

    def validate_volume(self, volume):
        """
        Validate whether an EBS volume is safe
        for cleanup recommendation.

        Conditions:
        - Volume state must be 'available'
        - Volume must have no attachments
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
        Return Elastic IPs that are potentially unused.
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

        Condition:
        - InstanceId must be None.
        """

        return address.get("InstanceId") is None

    # --------------------------------------------------
    # EC2
    # --------------------------------------------------

    def validate_instance(self, instance):
        """
        Validate EC2 instance information.

        This method does not terminate the instance.

        Returns True when the instance contains the
        required information for further cleanup analysis.
        """

        instance_id = instance.get("InstanceId")
        state = instance.get("State")

        return (
            instance_id is not None
            and state is not None
        )