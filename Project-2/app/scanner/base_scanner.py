class BaseScanner:
    """
    Base class for all AWS resource scanners.
    """

    def scan(self):
        raise NotImplementedError("Each scanner must implement the scan() method.")