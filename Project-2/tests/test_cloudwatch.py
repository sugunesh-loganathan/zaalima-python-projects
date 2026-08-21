from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

from aws.cloudwatch import CloudWatchService
from aws.exceptions import AWSAuthenticationError


def create_cloudwatch_service():

    client_factory = MagicMock()

    mock_cloudwatch_client = MagicMock()

    client_factory.get_client.return_value = mock_cloudwatch_client

    service = CloudWatchService(client_factory)

    return service, mock_cloudwatch_client


# ============================================================
# TEST 1 - FETCH CPU UTILIZATION
# ============================================================

def test_cloudwatch_fetches_cpu_utilization():

    service, mock_client = create_cloudwatch_service()

    mock_client.get_metric_statistics.return_value = {
        "Datapoints": [
            {
                "Average": 25.5
            },
            {
                "Average": 35.5
            }
        ],
        "Label": "CPUUtilization"
    }

    response = service.get_cpu_utilization(
        "i-test-123"
    )

    assert response["Label"] == "CPUUtilization"

    assert len(response["Datapoints"]) == 2

    mock_client.get_metric_statistics.assert_called_once()


# ============================================================
# TEST 2 - VERIFY CLOUDWATCH PARAMETERS
# ============================================================

def test_cloudwatch_uses_correct_parameters():

    service, mock_client = create_cloudwatch_service()

    mock_client.get_metric_statistics.return_value = {
        "Datapoints": []
    }

    service.get_cpu_utilization(
        "i-test-123"
    )

    kwargs = mock_client.get_metric_statistics.call_args.kwargs

    assert kwargs["Namespace"] == "AWS/EC2"

    assert kwargs["MetricName"] == "CPUUtilization"

    assert kwargs["Dimensions"] == [
        {
            "Name": "InstanceId",
            "Value": "i-test-123"
        }
    ]

    assert kwargs["Period"] == 86400

    assert kwargs["Statistics"] == ["Average"]


# ============================================================
# TEST 3 - AVERAGE CPU
# ============================================================

def test_cloudwatch_calculates_average_cpu():

    service, mock_client = create_cloudwatch_service()

    mock_client.get_metric_statistics.return_value = {
        "Datapoints": [
            {
                "Average": 20.0
            },
            {
                "Average": 40.0
            },
            {
                "Average": 60.0
            }
        ]
    }

    average = service.get_average_cpu(
        "i-test-123"
    )

    assert average == 40.0


# ============================================================
# TEST 4 - EMPTY DATAPOINTS
# ============================================================

def test_cloudwatch_returns_zero_for_empty_datapoints():

    service, mock_client = create_cloudwatch_service()

    mock_client.get_metric_statistics.return_value = {
        "Datapoints": []
    }

    average = service.get_average_cpu(
        "i-test-123"
    )

    assert average == 0.0


# ============================================================
# TEST 5 - ROUND AVERAGE CPU
# ============================================================

def test_cloudwatch_rounds_average_cpu():

    service, mock_client = create_cloudwatch_service()

    mock_client.get_metric_statistics.return_value = {
        "Datapoints": [
            {
                "Average": 10.123
            },
            {
                "Average": 20.456
            },
            {
                "Average": 30.789
            }
        ]
    }

    average = service.get_average_cpu(
        "i-test-123"
    )

    expected = round(
        (10.123 + 20.456 + 30.789) / 3,
        2
    )

    assert average == expected


# ============================================================
# TEST 6 - AWS ERROR HANDLING
# ============================================================

def test_cloudwatch_handles_aws_error():

    service, mock_client = create_cloudwatch_service()

    error = ClientError(
        {
            "Error": {
                "Code": "AccessDenied",
                "Message": "CloudWatch access denied"
            }
        },
        "GetMetricStatistics"
    )

    mock_client.get_metric_statistics.side_effect = error

    with pytest.raises(AWSAuthenticationError):

        service.get_cpu_utilization(
            "i-test-123"
        )