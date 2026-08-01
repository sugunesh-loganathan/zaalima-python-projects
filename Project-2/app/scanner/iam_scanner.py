from app.scanner.base_scanner import BaseScanner


class IAMScanner(BaseScanner):

    def scan(self):
        print("Scanning IAM resources...")