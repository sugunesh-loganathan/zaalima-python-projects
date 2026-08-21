from unittest.mock import MagicMock, patch

from aws.ebs import EBSService


def create_ebs_service():

    client_factory = MagicMock()

    mock_client = MagicMock()

    client_factory.get_client.return_value = mock_client

    service = EBSService(client_factory)

    return service, mock_client


def test_ebs_service_fetches_volumes():

    service, mock_client = create_ebs_service()

    mock_pages = [
        {
            "Volumes": [
                {
                    "VolumeId": "vol-test123",
                    "Size": 20,
                    "State": "available",
                    "VolumeType": "gp3",
                    "AvailabilityZone": "ap-south-1a",
                    "Encrypted": True,
                    "Attachments": []
                }
            ]
        }
    ]

    with patch(
        "aws.ebs.AWSPaginator.paginate",
        return_value=mock_pages
    ) as mock_paginate:

        response = service.get_volumes()

    assert "Volumes" in response
    assert len(response["Volumes"]) == 1

    assert response["Volumes"][0]["VolumeId"] == "vol-test123"

    mock_paginate.assert_called_once_with(
        "describe_volumes"
    )


def test_ebs_service_list_volumes():

    service, mock_client = create_ebs_service()

    mock_response = {
        "Volumes": [
            {
                "VolumeId": "vol-test123",
                "Size": 20,
                "State": "available",
                "VolumeType": "gp3",
                "AvailabilityZone": "ap-south-1a",
                "Encrypted": True,
                "Attachments": []
            }
        ]
    }

    with patch.object(
        service,
        "get_volumes",
        return_value=mock_response
    ):

        volumes = service.list_volumes()

    assert len(volumes) == 1

    volume = volumes[0]

    assert volume["VolumeId"] == "vol-test123"
    assert volume["Size"] == 20
    assert volume["State"] == "available"
    assert volume["VolumeType"] == "gp3"
    assert volume["AvailabilityZone"] == "ap-south-1a"
    assert volume["Encrypted"] is True
    assert volume["Attachments"] == 0


def test_ebs_service_handles_multiple_volumes():

    service, mock_client = create_ebs_service()

    mock_response = {
        "Volumes": [
            {
                "VolumeId": "vol-test001",
                "Size": 20,
                "State": "available",
                "VolumeType": "gp3",
                "AvailabilityZone": "ap-south-1a",
                "Encrypted": True,
                "Attachments": []
            },
            {
                "VolumeId": "vol-test002",
                "Size": 50,
                "State": "in-use",
                "VolumeType": "gp2",
                "AvailabilityZone": "ap-south-1b",
                "Encrypted": False,
                "Attachments": [
                    {
                        "InstanceId": "i-test123"
                    }
                ]
            }
        ]
    }

    with patch.object(
        service,
        "get_volumes",
        return_value=mock_response
    ):

        volumes = service.list_volumes()

    assert len(volumes) == 2

    assert volumes[0]["VolumeId"] == "vol-test001"
    assert volumes[0]["Attachments"] == 0

    assert volumes[1]["VolumeId"] == "vol-test002"
    assert volumes[1]["Attachments"] == 1


def test_ebs_service_detects_unattached_volumes():

    service, mock_client = create_ebs_service()

    volumes = [
        {
            "VolumeId": "vol-unattached",
            "Size": 20,
            "State": "available",
            "VolumeType": "gp3",
            "AvailabilityZone": "ap-south-1a",
            "Encrypted": True,
            "Attachments": 0
        },
        {
            "VolumeId": "vol-attached",
            "Size": 50,
            "State": "in-use",
            "VolumeType": "gp3",
            "AvailabilityZone": "ap-south-1b",
            "Encrypted": True,
            "Attachments": 1
        }
    ]

    unattached = service.get_unattached_volumes(volumes)

    assert len(unattached) == 1

    assert unattached[0]["VolumeId"] == "vol-unattached"


def test_ebs_service_handles_no_unattached_volumes():

    service, mock_client = create_ebs_service()

    volumes = [
        {
            "VolumeId": "vol-attached1",
            "Size": 20,
            "State": "in-use",
            "VolumeType": "gp3",
            "AvailabilityZone": "ap-south-1a",
            "Encrypted": True,
            "Attachments": 1
        },
        {
            "VolumeId": "vol-attached2",
            "Size": 50,
            "State": "in-use",
            "VolumeType": "gp3",
            "AvailabilityZone": "ap-south-1b",
            "Encrypted": False,
            "Attachments": 1
        }
    ]

    unattached = service.get_unattached_volumes(volumes)

    assert unattached == []


def test_ebs_service_handles_empty_response():

    service, mock_client = create_ebs_service()

    mock_response = {
        "Volumes": []
    }

    with patch.object(
        service,
        "get_volumes",
        return_value=mock_response
    ):

        volumes = service.list_volumes()

    assert volumes == []