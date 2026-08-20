import csv
import os


def export_csv(scan_data, filename="reports/scan_report.csv"):
    os.makedirs("reports", exist_ok=True)

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total Resources", scan_data["total_resources"]])
        writer.writerow(["Passed", scan_data["passed"]])
        writer.writerow(["Warnings", scan_data["warnings"]])
        writer.writerow(["Critical", scan_data["critical"]])

    print(f"CSV Report exported successfully -> {filename}")