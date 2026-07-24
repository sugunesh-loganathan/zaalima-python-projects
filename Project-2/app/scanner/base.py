"""
Base scanner for all AWS scanners.
"""


class BaseScanner:
    """Base class for all AWS resource scanners."""

    def scan(self):
        raise NotImplementedError("Subclasses must implement scan().")