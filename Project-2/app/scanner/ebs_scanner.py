from app.scanner.base_scanner import BaseScanner


class EBSScanner(BaseScanner):

    def scan(self):
        print("Scanning EBS volumes...")