from datetime import datetime, timedelta, UTC

from botocore.exceptions import ClientError

from aws.client_factory import AWSClientFactory
from aws.exceptions import AWSAuthenticationError
from utils.logger import logger
from utils.retry import aws_retry


class CloudWatchService:
    """
    Service class for CloudWatch metrics.
    """

    def __init__(self, client_factory: AWSClientFactory):
        self.client = client_factory.get_client("cloudwatch")

    @aws_retry()
    def get_cpu_utilization(self, instance_id):

        try:
            end_time = datetime.now(UTC)

            start_time = end_time - timedelta(days=14)

            response = self.client.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[
                    {
                        "Name": "InstanceId",
                        "Value": instance_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,
                Statistics=["Average"]
            )

            logger.info(f"CPU metrics fetched for {instance_id}")

            return response

        except ClientError as e:

            logger.error(f"CloudWatch Error: {e}")

            raise AWSAuthenticationError(str(e))

    def get_average_cpu(self, instance_id):

        response = self.get_cpu_utilization(instance_id)

        datapoints = response["Datapoints"]

        if not datapoints:
            return 0.0

        total = sum(point["Average"] for point in datapoints)

        return round(total / len(datapoints), 2)