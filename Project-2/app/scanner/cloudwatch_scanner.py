"""
CloudWatch Scanner Module

"""


from .base import BaseScanner


class CloudWatchScanner(BaseScanner):
    """Scanner for CloudWatch metrics."""

    def scan(self):
        self.logger.info("CloudWatch scan started.")
        return []