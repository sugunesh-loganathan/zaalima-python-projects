from app.scanner.base_scanner import BaseScanner


class S3Scanner(BaseScanner):

    def scan(self):
        print("Scanning S3 buckets...")