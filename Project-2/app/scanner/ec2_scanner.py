from app.scanner.base_scanner import BaseScanner


class EC2Scanner(BaseScanner):

    def scan(self):
        """
        Simulate scanning EC2 instances.
        """

        return {
            "service": "EC2",
            "status": "success",
            "resources_found": 0,
            "message": "No EC2 instances found."
        }