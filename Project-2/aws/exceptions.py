class AWSAuthenticationError(Exception):
    """
    Raised when AWS authentication or authorization fails.
    """
    pass


class AWSCleanupError(Exception):
    """
    Raised when an AWS cleanup operation fails.
    """
    pass