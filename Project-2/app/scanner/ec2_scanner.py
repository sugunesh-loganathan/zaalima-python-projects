from app.scanner.base_scanner import BaseScanner
from app.models.scan_result import ScanResult


class EC2Scanner(BaseScanner):

    def scan(self):
        """
        Simulate scanning EC2 instances.
        """

        result = ScanResult(
            service="EC2",
            status="success",
            resources_found=0,
            message="No EC2 instances found."
        )

        return result.to_dict()