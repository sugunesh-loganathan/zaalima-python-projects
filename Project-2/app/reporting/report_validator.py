import csv
import json
from pathlib import Path


REPORTS_DIR = Path("reports")

CSV_FILE = REPORTS_DIR / "scan_report.csv"
JSON_FILE = REPORTS_DIR / "scan_report.json"


def validate_csv():
    if not CSV_FILE.exists():
        return False, "CSV report not found"

    try:
        with open(CSV_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        required_columns = {"Metric", "Value"}

        if not required_columns.issubset(reader.fieldnames or set()):
            return False, "CSV columns are invalid"

        if not rows:
            return False, "CSV report is empty"

        return True, "CSV report is valid"

    except Exception as error:
        return False, f"CSV validation failed: {error}"


def validate_json():
    if not JSON_FILE.exists():
        return False, "JSON report not found"

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        required_fields = {
            "total_resources",
            "passed",
            "warnings",
            "critical",
            "recommendations",
        }

        if not required_fields.issubset(data.keys()):
            return False, "JSON fields are invalid"

        if not isinstance(data["recommendations"], list):
            return False, "Recommendations must be a list"

        return True, "JSON report is valid"

    except json.JSONDecodeError:
        return False, "JSON file contains invalid JSON"

    except Exception as error:
        return False, f"JSON validation failed: {error}"


def validate_reports():
    print("\n========== REPORT VALIDATION ==========\n")

    csv_valid, csv_message = validate_csv()
    json_valid, json_message = validate_json()

    if csv_valid:
        print("✓ CSV:", csv_message)
    else:
        print("✗ CSV:", csv_message)

    if json_valid:
        print("✓ JSON:", json_message)
    else:
        print("✗ JSON:", json_message)

    if csv_valid and json_valid:
        print("\n✓ All exported reports passed validation.")
        return True

    print("\n✗ Report validation failed.")
    return False