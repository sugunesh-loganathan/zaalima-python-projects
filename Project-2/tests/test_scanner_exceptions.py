"""
Tests for AWS scanner exception handling.
"""

import unittest
from unittest.mock import Mock

from botocore.exceptions import BotoCoreError, ClientError

from app.scanner.ec2_scanner import EC2Scanner
from app.scanner.ebs_scanner import EBSScanner
from app.scanner.elastic_ip_scanner import ElasticIPScanner
from app.scanner.exceptions import ScannerException


class TestScannerExceptions(unittest.TestCase):
    """Test scanner AWS API exception handling."""

    def create_client_error(self):
        """Create a sample AWS ClientError."""
        return ClientError(
            {
                "Error": {
                    "Code": "AccessDenied",
                    "Message": "Access denied"
                }
            },
            "DescribeResources"
        )

    def test_ec2_client_error_is_handled(self):
        """EC2 ClientError should be converted to ScannerException."""
        scanner = EC2Scanner()

        mock_client = Mock()
        mock_client.describe_instances.side_effect = (
            self.create_client_error()
        )

        scanner.get_client = Mock(return_value=mock_client)

        with self.assertRaises(ScannerException):
            scanner.scan()

    def test_ebs_client_error_is_handled(self):
        """EBS ClientError should be converted to ScannerException."""
        scanner = EBSScanner()

        mock_client = Mock()
        mock_client.describe_volumes.side_effect = (
            self.create_client_error()
        )

        scanner.get_client = Mock(return_value=mock_client)

        with self.assertRaises(ScannerException):
            scanner.scan()

    def test_elastic_ip_client_error_is_handled(self):
        """Elastic IP ClientError should be converted to ScannerException."""
        scanner = ElasticIPScanner()

        mock_client = Mock()
        mock_client.describe_addresses.side_effect = (
            self.create_client_error()
        )

        scanner.get_client = Mock(return_value=mock_client)

        with self.assertRaises(ScannerException):
            scanner.scan()

    def test_ec2_boto_core_error_is_handled(self):
        """EC2 BotoCoreError should be converted to ScannerException."""
        scanner = EC2Scanner()

        mock_client = Mock()
        mock_client.describe_instances.side_effect = (
            BotoCoreError()
        )

        scanner.get_client = Mock(return_value=mock_client)

        with self.assertRaises(ScannerException):
            scanner.scan()

    def test_ebs_boto_core_error_is_handled(self):
        """EBS BotoCoreError should be converted to ScannerException."""
        scanner = EBSScanner()

        mock_client = Mock()
        mock_client.describe_volumes.side_effect = (
            BotoCoreError()
        )

        scanner.get_client = Mock(return_value=mock_client)

        with self.assertRaises(ScannerException):
            scanner.scan()


if __name__ == "__main__":
    unittest.main()