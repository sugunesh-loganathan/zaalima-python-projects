"""
Custom exceptions for the Scanner Package.
"""


class ScannerException(Exception):
    """Base exception for all scanner errors."""


class AuthenticationError(ScannerException):
    """Raised when AWS authentication fails."""


class PermissionError(ScannerException):
    """Raised when AWS permissions are insufficient."""


class ResourceScanError(ScannerException):
    """Raised when an AWS resource scan fails."""


class RateLimitError(ScannerException):
    """Raised when AWS API rate limits are exceeded."""