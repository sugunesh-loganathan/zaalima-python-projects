import json
import os


def export_json(scan_data, filename="reports/scan_report.json"):
    os.makedirs("reports", exist_ok=True)

    with open(filename, "w") as file:
        json.dump(scan_data, file, indent=4)

    print(f"JSON Report exported successfully -> {filename}")