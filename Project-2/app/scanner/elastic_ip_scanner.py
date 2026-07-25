"""
Elastic IP Scanner Module
"""

from .base import BaseScanner


class ElasticIPScanner(BaseScanner):
    """Scanner for Elastic IP resources."""

    def scan(self):
        self.logger.info("Elastic IP scan started.")
        return []