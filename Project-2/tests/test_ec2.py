from unittest.mock import MagicMock, patch

from aws.ec2 import EC2Service


def create_ec2_service():

    client_factory = MagicMock()

    mock_client = MagicMock()

    client_factory.get_client.return_value = mock_client

    service = EC2Service(client_factory)

    return service, mock_client


def test_ec2_service_fetches_instances():

    service, mock_client = create_ec2_service()

    mock_pages = [
        {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-test123",
                            "InstanceType": "t2.micro",
                            "State": {
                                "Name": "running"
                            },
                            "Placement": {
                                "AvailabilityZone": "ap-south-1a"
                            },
                            "PrivateIpAddress": "10.0.0.10",
                            "PublicIpAddress": "1.2.3.4"
                        }
                    ]
                }
            ]
        }
    ]

    with patch(
        "aws.ec2.AWSPaginator.paginate",
        return_value=mock_pages
    ) as mock_paginate:

        response = service.get_instances()

    assert "Reservations" in response
    assert len(response["Reservations"]) == 1

    mock_paginate.assert_called_once_with(
        "describe_instances"
    )


def test_ec2_service_list_instances():

    service, mock_client = create_ec2_service()

    mock_response = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-test123",
                        "InstanceType": "t2.micro",
                        "State": {
                            "Name": "running"
                        },
                        "Placement": {
                            "AvailabilityZone": "ap-south-1a"
                        },
                        "PrivateIpAddress": "10.0.0.10",
                        "PublicIpAddress": "1.2.3.4"
                    }
                ]
            }
        ]
    }

    with patch.object(
        service,
        "get_instances",
        return_value=mock_response
    ):

        instances = service.list_instances()

    assert len(instances) == 1

    instance = instances[0]

    assert instance["InstanceId"] == "i-test123"
    assert instance["InstanceType"] == "t2.micro"
    assert instance["State"] == "running"
    assert instance["AvailabilityZone"] == "ap-south-1a"
    assert instance["PrivateIP"] == "10.0.0.10"
    assert instance["PublicIP"] == "1.2.3.4"


def test_ec2_service_handles_multiple_instances():

    service, mock_client = create_ec2_service()

    mock_response = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-test001",
                        "InstanceType": "t2.micro",
                        "State": {
                            "Name": "running"
                        },
                        "Placement": {
                            "AvailabilityZone": "ap-south-1a"
                        }
                    },
                    {
                        "InstanceId": "i-test002",
                        "InstanceType": "t3.micro",
                        "State": {
                            "Name": "stopped"
                        },
                        "Placement": {
                            "AvailabilityZone": "ap-south-1b"
                        }
                    }
                ]
            }
        ]
    }

    with patch.object(
        service,
        "get_instances",
        return_value=mock_response
    ):

        instances = service.list_instances()

    assert len(instances) == 2

    assert instances[0]["InstanceId"] == "i-test001"
    assert instances[0]["State"] == "running"

    assert instances[1]["InstanceId"] == "i-test002"
    assert instances[1]["State"] == "stopped"


def test_ec2_service_handles_empty_response():

    service, mock_client = create_ec2_service()

    mock_response = {
        "Reservations": []
    }

    with patch.object(
        service,
        "get_instances",
        return_value=mock_response
    ):

        instances = service.list_instances()

    assert instances == []