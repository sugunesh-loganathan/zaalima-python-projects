"""
Tests for the Cleanup Recommendation Module.
"""

import unittest

from app.scanner.cleanup_recommender import CleanupRecommender


class TestCleanupRecommender(unittest.TestCase):
    """Test cleanup recommendation logic."""

    def setUp(self):
        """Create a cleanup recommender for each test."""
        self.recommender = CleanupRecommender()

    def test_unattached_ebs_is_unused(self):
        """Unattached EBS volume should be detected as unused."""
        resource = {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "status": "available",
            "details": {
                "attached": False
            }
        }

        self.assertTrue(
            self.recommender.is_unused_resource(resource)
        )

    def test_attached_ebs_is_not_unused(self):
        """Attached EBS volume should not be detected as unused."""
        resource = {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "status": "in-use",
            "details": {
                "attached": True
            }
        }

        self.assertFalse(
            self.recommender.is_unused_resource(resource)
        )

    def test_unassociated_elastic_ip_is_unused(self):
        """Unassociated Elastic IP should be detected as unused."""
        resource = {
            "resource_type": "ElasticIP",
            "resource_id": "eipalloc-123",
            "status": "Unassociated",
            "details": {}
        }

        self.assertTrue(
            self.recommender.is_unused_resource(resource)
        )

    def test_associated_elastic_ip_is_not_unused(self):
        """Associated Elastic IP should not be detected as unused."""
        resource = {
            "resource_type": "ElasticIP",
            "resource_id": "eipalloc-123",
            "status": "Associated",
            "details": {}
        }

        self.assertFalse(
            self.recommender.is_unused_resource(resource)
        )

    def test_low_cpu_resource_is_idle(self):
        """EC2 resource with CPU below 5 percent should be idle."""
        resource = {
            "resource_type": "CloudWatch",
            "resource_id": "i-123",
            "status": "Low Utilization",
            "details": {
                "average_cpu_percent": 3.5
            }
        }

        self.assertTrue(
            self.recommender.is_idle_resource(resource)
        )

    def test_normal_cpu_resource_is_not_idle(self):
        """EC2 resource with CPU at or above 5 percent is not idle."""
        resource = {
            "resource_type": "CloudWatch",
            "resource_id": "i-123",
            "status": "Normal",
            "details": {
                "average_cpu_percent": 10.0
            }
        }

        self.assertFalse(
            self.recommender.is_idle_resource(resource)
        )

    def test_missing_cpu_data_is_not_idle(self):
        """Missing CPU data should not be treated as idle."""
        resource = {
            "resource_type": "CloudWatch",
            "resource_id": "i-123",
            "status": "Normal",
            "details": {
                "average_cpu_percent": None
            }
        }

        self.assertFalse(
            self.recommender.is_idle_resource(resource)
        )

    def test_ebs_cleanup_recommendation(self):
        """Unattached EBS should receive a cleanup recommendation."""
        resource = {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "status": "available",
            "details": {
                "attached": False
            }
        }

        recommendation, priority = (
            self.recommender.get_recommendation(resource)
        )

        self.assertEqual(priority, "High")
        self.assertIn("EBS", recommendation)

    def test_elastic_ip_cleanup_recommendation(self):
        """Unassociated Elastic IP should receive a recommendation."""
        resource = {
            "resource_type": "ElasticIP",
            "resource_id": "eipalloc-123",
            "status": "Unassociated",
            "details": {}
        }

        recommendation, priority = (
            self.recommender.get_recommendation(resource)
        )

        self.assertEqual(priority, "Medium")
        self.assertIn("Elastic IP", recommendation)

    def test_idle_ec2_recommendation(self):
        """Low CPU EC2 should receive an optimization recommendation."""
        resource = {
            "resource_type": "CloudWatch",
            "resource_id": "i-123",
            "status": "Low Utilization",
            "details": {
                "average_cpu_percent": 2.0
            }
        }

        recommendation, priority = (
            self.recommender.get_recommendation(resource)
        )

        self.assertEqual(priority, "Medium")
        self.assertIn("EC2", recommendation)

    def test_normal_resource_requires_no_action(self):
        """Normal resources should not receive a cleanup action."""
        resource = {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "status": "in-use",
            "details": {
                "attached": True
            }
        }

        recommendation, priority = (
            self.recommender.get_recommendation(resource)
        )

        self.assertEqual(priority, "Low")
        self.assertEqual(
            recommendation,
            "No action required."
        )


if __name__ == "__main__":
    unittest.main()