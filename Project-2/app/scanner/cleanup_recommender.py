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

    def recommend(self, scan_results):
        """
        Generate cleanup recommendations for scanned resources.
        """
        recommendations = []

        for resource in scan_results:
            unused = self.is_unused_resource(resource)

            recommendation = {
                "resource_type": resource.get("resource_type"),
                "resource_id": resource.get("resource_id"),
                "unused": unused,
                "recommendation": (
                    "Review resource for cleanup"
                    if unused
                    else "No action required"
                ),
            }

            recommendations.append(recommendation)

        self.logger.info(
            "Unused resource detection completed."
        )

        return recommendations