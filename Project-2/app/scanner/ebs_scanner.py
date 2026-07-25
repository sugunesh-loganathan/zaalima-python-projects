"""
EBS Scanner Module
"""

from .base import BaseScanner


class EBSScanner(BaseScanner):
    """Scanner for EBS resources."""

    def scan(self):
        self.logger.info("EBS scan started.")
        return []
