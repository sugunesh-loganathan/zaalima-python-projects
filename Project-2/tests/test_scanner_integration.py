"""
Integration tests for the scanner and cleanup recommendation workflow.
"""

import unittest

from app.scanner.cleanup_recommender import CleanupRecommender


class TestScannerIntegration(unittest.TestCase):
    """Test integration of scanner results with cleanup recommendations."""

    def setUp(self):
        """Create a cleanup recommender for each test."""
        self.recommender = CleanupRecommender()

    def test_multiple_scanner_results_are_processed(self):
        """Multiple resource scan results should be processed together."""

        scan_results = [
            {
                "resource_type": "EBS",
                "resource_id": "vol-001",
                "status": "available",
                "details": {
                    "attached": False
                }
            },
            {
                "resource_type": "EBS",
                "resource_id": "vol-002",
                "status": "in-use",
                "details": {
                    "attached": True
                }
            },
            {
                "resource_type": "ElasticIP",
                "resource_id": "eip-001",
                "status": "Unassociated",
                "details": {}
            },
            {
                "resource_type": "CloudWatch",
                "resource_id": "i-001",
                "status": "Low Utilization",
                "details": {
                    "average_cpu_percent": 2.5
                }
            }
        ]

        recommendations = self.recommender.recommend(scan_results)

        self.assertEqual(len(recommendations), 4)

    def test_recommendations_match_resource_types(self):
        """Recommendations should correspond to the correct resources."""

        scan_results = [
            {
                "resource_type": "EBS",
                "resource_id": "vol-001",
                "status": "available",
                "details": {
                    "attached": False
                }
            },
            {
                "resource_type": "ElasticIP",
                "resource_id": "eip-001",
                "status": "Unassociated",
                "details": {}
            },
            {
                "resource_type": "CloudWatch",
                "resource_id": "i-001",
                "status": "Low Utilization",
                "details": {
                    "average_cpu_percent": 2.5
                }
            }
        ]

        recommendations = self.recommender.recommend(scan_results)

        self.assertEqual(
            recommendations[0]["resource_type"],
            "EBS"
        )

        self.assertEqual(
            recommendations[1]["resource_type"],
            "ElasticIP"
        )

        self.assertEqual(
            recommendations[2]["resource_type"],
            "CloudWatch"
        )

    def test_cleanup_recommendations_are_generated(self):
        """Unused and idle resources should receive recommendations."""

        scan_results = [
            {
                "resource_type": "EBS",
                "resource_id": "vol-001",
                "status": "available",
                "details": {
                    "attached": False
                }
            },
            {
                "resource_type": "ElasticIP",
                "resource_id": "eip-001",
                "status": "Unassociated",
                "details": {}
            },
            {
                "resource_type": "CloudWatch",
                "resource_id": "i-001",
                "status": "Low Utilization",
                "details": {
                    "average_cpu_percent": 2.5
                }
            }
        ]

        recommendations = self.recommender.recommend(scan_results)

        self.assertIn(
            "Review unattached EBS volume for deletion.",
            recommendations[0]["recommendation"]
        )

        self.assertIn(
            "Review unassociated Elastic IP for release.",
            recommendations[1]["recommendation"]
        )

        self.assertIn(
            "Review EC2 instance",
            recommendations[2]["recommendation"]
        )

    def test_active_resource_requires_no_action(self):
        """An active EBS resource should require no cleanup action."""

        scan_results = [
            {
                "resource_type": "EBS",
                "resource_id": "vol-active",
                "status": "in-use",
                "details": {
                    "attached": True
                }
            }
        ]

        recommendations = self.recommender.recommend(scan_results)

        self.assertEqual(
            recommendations[0]["recommendation"],
            "No action required."
        )

        self.assertEqual(
            recommendations[0]["priority"],
            "Low"
        )


if __name__ == "__main__":
    unittest.main()