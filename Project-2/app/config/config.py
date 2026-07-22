"""
Project Configuration
Cloud Infrastructure Auditor & Cost Optimizer (CLI)
"""

from dataclasses import dataclass

@dataclass
class Settings:
    PROJECT_NAME = "Cloud Infrastructure Auditor & Cost Optimizer (CLI)"
    VERSION = "1.0.0"

    DEFAULT_REGION = "ap-south-1"

    REPORT_FOLDER = "reports"

    LOG_LEVEL = "INFO"

settings = Settings()