"""
Cleanup Recommendation Module
"""

from .base import BaseScanner


class CleanupRecommender(BaseScanner):
    """Generate cleanup recommendations for scanned AWS resources."""

    def is_unused_resource(self, resource):
        """
        Check whether a scanned AWS resource is unused.
        """
        resource_type = resource.get("resource_type")
        status = resource.get("status")
        details = resource.get("details", {})

        if resource_type == "EBS":
            return not details.get("attached", False)

        if resource_type == "ElasticIP":
            return status == "Unassociated"

        return False

    def is_idle_resource(self, resource):
        """
        Check whether a scanned AWS resource is idle.
        """
        if resource.get("resource_type") != "CloudWatch":
            return False

        average_cpu = resource.get("details", {}).get(
            "average_cpu_percent"
        )

        if average_cpu is None:
            return False

        return average_cpu < 5

    def get_recommendation(self, resource):
        """
        Return a cleanup recommendation based on resource type.
        """
        resource_type = resource.get("resource_type")

        if self.is_unused_resource(resource):

            if resource_type == "EBS":
                return "Review unattached EBS volume for deletion."

            if resource_type == "ElasticIP":
                return "Review unassociated Elastic IP for release."

        if self.is_idle_resource(resource):
            return (
                "Review EC2 instance for stopping or rightsizing "
                "due to low CPU utilization."
            )

        return "No action required."

    def recommend(self, scan_results):
        """
        Generate cleanup recommendations.
        """
        recommendations = []

        for resource in scan_results:

            recommendations.append({
                "resource_type": resource.get("resource_type"),
                "resource_id": resource.get("resource_id"),
                "recommendation": self.get_recommendation(resource),
            })

        self.logger.info(
            "Cleanup recommendation engine completed."
        )

        return recommendations