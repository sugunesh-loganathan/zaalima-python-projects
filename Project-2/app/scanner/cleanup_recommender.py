"""
Cleanup Recommendation Module
"""

from .base import BaseScanner


class CleanupRecommender(BaseScanner):
    """Generate cleanup recommendations for scanned AWS resources."""

    def recommend(self, scan_results):
        """
        Generate cleanup recommendations based on scan results.
        """
        recommendations = []

        for resource in scan_results:

            recommendation = {
                "resource_type": resource.get("resource_type"),
                "resource_id": resource.get("resource_id"),
                "recommendation": "No action required"
            }

            recommendations.append(recommendation)

        self.logger.info("Cleanup recommendations generated.")

        return recommendations