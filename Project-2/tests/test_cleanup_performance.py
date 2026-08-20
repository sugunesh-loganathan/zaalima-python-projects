"""
Performance tests for the Cleanup Recommendation Module.
"""

import time
import unittest

from app.scanner.cleanup_recommender import CleanupRecommender


class TestCleanupPerformance(unittest.TestCase):
    """Performance tests for cleanup recommendations."""

    def test_cleanup_recommendation_performance(self):
        """
        Measure cleanup recommendation processing time.
        """
        recommender = CleanupRecommender()

        scan_results = []

        # Create 1000 sample scan results.
        for index in range(1000):
            scan_results.append({
                "resource_type": "EBS",
                "resource_id": f"vol-test-{index}",
                "status": "available",
                "details": {
                    "attached": False
                }
            })

        start_time = time.perf_counter()

        recommendations = recommender.recommend(scan_results)

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        self.assertEqual(len(recommendations), 1000)

        print(
            f"\nProcessed 1000 resources in "
            f"{elapsed_time:.6f} seconds"
        )

        # The recommendation engine should process
        # 1000 simple results within 1 second.
        self.assertLess(elapsed_time, 1.0)


if __name__ == "__main__":
    unittest.main()