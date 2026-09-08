from app.scanner.ec2_scanner import EC2Scanner
from app.scanner.ebs_scanner import EBSScanner


class ScannerManager:
    """
    Manages all AWS resource scanners.
    """

    def __init__(self):
        self.scanners = [
            EC2Scanner(),
            EBSScanner(),
        ]

    def scan_all(self):
        results = []

        for scanner in self.scanners:
            results.append(scanner.scan())

        return results