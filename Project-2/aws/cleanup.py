from aws.ebs import EBSService
from aws.eip import ElasticIPService


class CleanupService:
    """
    Cleanup support service.

    Provides validation and cleanup recommendations.
    No AWS resources are deleted in this module.
    """

    def __init__(self, client_factory):
        self.ebs_service = EBSService(client_factory)
        self.eip_service = ElasticIPService(client_factory)

    def get_unused_volumes(self):
        """
        Return unattached EBS volumes.
        """
        volumes = self.ebs_service.list_volumes()
        return self.ebs_service.get_unattached_volumes(volumes)

    def get_unused_elastic_ips(self):
        """
        Return unassociated Elastic IPs.
        """
        addresses = self.eip_service.list_addresses()
        return self.eip_service.get_unassociated_addresses(addresses)