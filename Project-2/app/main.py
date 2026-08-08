"""
Application Entry Point
Starts the Cloud Infrastructure Auditor
Reporting Module.
"""

from app.reporting.report_generator import generate_report


if __name__ == "__main__":
    generate_report()