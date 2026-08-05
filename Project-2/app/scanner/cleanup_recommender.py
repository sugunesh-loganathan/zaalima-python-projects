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

        # Detect unattached EBS volumes
        if resource_type == "EBS":
            return not details.get("attached", False)

        # Detect unassociated Elastic IP addresses
        if resource_type == "ElasticIP":
            return status == "Unassociated"

        return False

    def is_idle_resource(self, resource):
        """
        Check whether an EC2 resource has low CPU utilization.
        """
        resource_type = resource.get("resource_type")
        details = resource.get("details", {})

        if resource_type != "CloudWatch":
            return False

        average_cpu = details.get("average_cpu_percent")

        if average_cpu is None:
            return False

        return average_cpu < 5

    def recommend(self, scan_results):
        """
        Generate cleanup recommendations for scanned resources.
        """
        recommendations = []

        for resource in scan_results:
            unused = self.is_unused_resource(resource)
            idle = self.is_idle_resource(resource)

            if unused:
                recommendation_text = "Review resource for cleanup"

            elif idle:
                recommendation_text = (
                    "Review idle EC2 instance for optimization"
                )

            else:
                recommendation_text = "No action required"

            recommendation = {
                "resource_type": resource.get("resource_type"),
                "resource_id": resource.get("resource_id"),
                "unused": unused,
                "idle": idle,
                "recommendation": recommendation_text,
            }

            recommendations.append(recommendation)

        self.logger.info(
            "Cleanup recommendations generated successfully."
        )

        return recommendations