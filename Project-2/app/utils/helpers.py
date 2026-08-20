"""
Helper Functions
"""

from datetime import datetime

def get_timestamp():
    """
    Returns current timestamp.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")