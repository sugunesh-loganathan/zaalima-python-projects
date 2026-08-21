"""
Validation Utilities
"""

def validate_region(region: str):

    if not region:
        raise ValueError("AWS region cannot be empty.")

    return True