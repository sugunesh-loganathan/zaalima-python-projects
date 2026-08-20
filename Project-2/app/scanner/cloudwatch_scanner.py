"""
CloudWatch Scanner Module
"""

from datetime import datetime, timedelta, timezone

from botocore.exceptions import BotoCoreError, ClientError

from .base import BaseScanner
from .exceptions import ScannerException


class CloudWatchScanner(BaseScanner):
    """Scanner for EC2 CloudWatch utilization metrics."""

    def get_cpu_utilization(self, instance_id, days=14):
        """
        Return the average CPU utilization of an EC2 instance.
        """
        try:
            client = self.get_client("cloudwatch")

            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(days=days)

            response = client.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[
                    {
                        "Name": "InstanceId",
                        "Value": instance_id,
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,
                Statistics=["Average"],
            )

            datapoints = response.get("Datapoints", [])

            if not datapoints:
                return None

            average_cpu = sum(
                point["Average"] for point in datapoints
            ) / len(datapoints)

            return round(average_cpu, 2)

        except (ClientError, BotoCoreError) as error:
            self.logger.error(
                f"CloudWatch scan failed for {instance_id}: {error}"
            )
            raise ScannerException(str(error))

    def scan(self, instance_ids=None):
        """
        Scan CPU utilization for the supplied EC2 instances.
        """
        results = []

        if not instance_ids:
            return results

        for instance_id in instance_ids:
            average_cpu = self.get_cpu_utilization(instance_id)

            results.append({
                "resource_type": "CloudWatch",
                "resource_id": instance_id,
                "status": (
                    "Low Utilization"
                    if average_cpu is not None and average_cpu < 5
                    else "Normal"
                ),
                "region": self.region_name,
                "details": {
                    "metric": "CPUUtilization",
                    "average_cpu_percent": average_cpu,
                    "period_days": 14,
                },
            })

        self.logger.info("CloudWatch utilization scan completed.")
        return results