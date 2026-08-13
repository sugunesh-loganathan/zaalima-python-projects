from datetime import datetime, timedelta, timezone

from app.scanner.base_scanner import BaseScanner
from app.models.scan_result import ScanResult
from app.aws.session import AWSSession

from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    ClientError,
)

from app.utils import logger


class EC2Scanner(BaseScanner):
    """
    Scanner for EC2 resources.
    """

    def __init__(self):
        self.session_manager = AWSSession()

    def get_client(self):
        """
        Create and return an EC2 boto3 client.
        """

        return self.session_manager.create_client("ec2")

    def get_cloudwatch_client(self):
        """
        Create and return a CloudWatch boto3 client.
        """

        return self.session_manager.create_client("cloudwatch")

    def get_cpu_utilization(self, instance_id):
        """
        Retrieve recent average CPU utilization for an EC2 instance.
        """

        cloudwatch = self.get_cloudwatch_client()

        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=1)

        response = cloudwatch.get_metric_statistics(
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
            Period=3600,
            Statistics=["Average"],
        )

        datapoints = response.get("Datapoints", [])

        if not datapoints:
            return None

        return round(datapoints[-1]["Average"], 2)

    def scan(self):
        """
        Discover and analyze EC2 instances.
        """

        logger.info("Starting EC2 resource scan...")

        try:
            ec2 = self.get_client()

            response = ec2.describe_instances()

            instances = []

            for reservation in response["Reservations"]:

                for instance in reservation["Instances"]:

                    instance_id = instance["InstanceId"]

                    cpu_utilization = self.get_cpu_utilization(
                        instance_id
                    )

                    instance_data = {
                        "instance_id": instance_id,
                        "state": instance["State"]["Name"],
                        "type": instance["InstanceType"],
                        "cpu_utilization": cpu_utilization,
                    }

                    instances.append(instance_data)

            # Analyze each instance
            for instance in instances:

                if instance["state"] == "stopped":

                    instance["recommendation"] = "Safe to terminate"

                elif instance["state"] == "running":

                    cpu = instance["cpu_utilization"]

                    if cpu is not None and cpu < 10:
                        instance["recommendation"] = "Underutilized"

                    elif cpu is None:
                        instance["recommendation"] = "Review required"

                    else:
                        instance["recommendation"] = "Healthy"

                else:

                    instance["recommendation"] = "Review required"

            logger.info(
                f"EC2 scan completed. Resources found: {len(instances)}"
            )

            result = ScanResult(
                service="EC2",
                status="success",
                resources_found=len(instances),
                message="EC2 scan completed successfully.",
            )

            return {
                **result.to_dict(),
                "instances": instances,
            }

        except NoCredentialsError:

            logger.error("AWS credentials not found.")

            result = ScanResult(
                service="EC2",
                status="failed",
                resources_found=0,
                message="AWS credentials not found.",
            )

            return result.to_dict()

        except PartialCredentialsError:

            logger.error("Incomplete AWS credentials.")

            result = ScanResult(
                service="EC2",
                status="failed",
                resources_found=0,
                message="Incomplete AWS credentials.",
            )

            return result.to_dict()

        except ClientError as e:

            logger.error(f"AWS EC2/CloudWatch API error: {e}")

            result = ScanResult(
                service="EC2",
                status="failed",
                resources_found=0,
                message=f"AWS EC2/CloudWatch API error: {e}",
            )

            return result.to_dict()

        except Exception as e:

            logger.error(f"Unexpected EC2 scanner error: {e}")

            result = ScanResult(
                service="EC2",
                status="failed",
                resources_found=0,
                message=f"Unexpected scanner error: {e}",
            )

            return result.to_dict()