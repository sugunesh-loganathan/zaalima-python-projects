from app.scanner.base_scanner import BaseScannerfr


class IAMScanner(BaseScanner):

    def scan(self):
        print("Scanning IAM resources...")