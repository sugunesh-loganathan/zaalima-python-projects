from app.scanner.base_scanner import BaseScanner


class EC2Scanner(BaseScanner):

    def scan(self):
        print("Scanning EC2 instances...")