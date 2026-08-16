from unittest.mock import MagicMock, patch

from aws.eip import ElasticIPService


def create_eip_service():

    client_factory = MagicMock()

    mock_client = MagicMock()

    client_factory.get_client.return_value = mock_client

    service = ElasticIPService(client_factory)

    return service, mock_client


def test_eip_service_fetches_addresses():

    service, mock_client = create_eip_service()

    mock_response = {
        "Addresses": [
            {
                "AllocationId": "eipalloc-test123",
                "PublicIp": "1.2.3.4",
                "PrivateIpAddress": "10.0.0.10",
                "InstanceId": "i-test123",
                "AssociationId": "eipassoc-test123",
                "Domain": "vpc"
            }
        ]
    }

    mock_client.describe_addresses.return_value = mock_response

    response = service.get_addresses()

    assert "Addresses" in response
    assert len(response["Addresses"]) == 1

    assert response["Addresses"][0]["AllocationId"] == "eipalloc-test123"

    mock_client.describe_addresses.assert_called_once_with()


def test_eip_service_list_addresses():

    service, mock_client = create_eip_service()

    mock_response = {
        "Addresses": [
            {
                "AllocationId": "eipalloc-test123",
                "PublicIp": "1.2.3.4",
                "PrivateIpAddress": "10.0.0.10",
                "InstanceId": "i-test123",
                "AssociationId": "eipassoc-test123",
                "Domain": "vpc"
            }
        ]
    }

    with patch.object(
        service,
        "get_addresses",
        return_value=mock_response
    ):

        addresses = service.list_addresses()

    assert len(addresses) == 1

    address = addresses[0]

    assert address["AllocationId"] == "eipalloc-test123"
    assert address["PublicIp"] == "1.2.3.4"
    assert address["PrivateIp"] == "10.0.0.10"
    assert address["InstanceId"] == "i-test123"
    assert address["AssociationId"] == "eipassoc-test123"
    assert address["Domain"] == "vpc"


def test_eip_service_handles_multiple_addresses():

    service, mock_client = create_eip_service()

    mock_response = {
        "Addresses": [
            {
                "AllocationId": "eipalloc-test001",
                "PublicIp": "1.2.3.4",
                "PrivateIpAddress": "10.0.0.10",
                "InstanceId": "i-test001",
                "AssociationId": "eipassoc-test001",
                "Domain": "vpc"
            },
            {
                "AllocationId": "eipalloc-test002",
                "PublicIp": "5.6.7.8",
                "PrivateIpAddress": None,
                "InstanceId": None,
                "AssociationId": None,
                "Domain": "vpc"
            }
        ]
    }

    with patch.object(
        service,
        "get_addresses",
        return_value=mock_response
    ):

        addresses = service.list_addresses()

    assert len(addresses) == 2

    assert addresses[0]["AllocationId"] == "eipalloc-test001"
    assert addresses[0]["InstanceId"] == "i-test001"

    assert addresses[1]["AllocationId"] == "eipalloc-test002"
    assert addresses[1]["InstanceId"] is None


def test_eip_service_detects_unassociated_addresses():

    service, mock_client = create_eip_service()

    addresses = [
        {
            "AllocationId": "eipalloc-unassociated",
            "PublicIp": "1.2.3.4",
            "PrivateIp": None,
            "InstanceId": None,
            "AssociationId": None,
            "Domain": "vpc"
        },
        {
            "AllocationId": "eipalloc-associated",
            "PublicIp": "5.6.7.8",
            "PrivateIp": "10.0.0.20",
            "InstanceId": "i-test123",
            "AssociationId": "eipassoc-test123",
            "Domain": "vpc"
        }
    ]

    unassociated = service.get_unassociated_addresses(addresses)

    assert len(unassociated) == 1

    assert unassociated[0]["AllocationId"] == "eipalloc-unassociated"
    assert unassociated[0]["InstanceId"] is None


def test_eip_service_handles_no_unassociated_addresses():

    service, mock_client = create_eip_service()

    addresses = [
        {
            "AllocationId": "eipalloc-test001",
            "PublicIp": "1.2.3.4",
            "PrivateIp": "10.0.0.10",
            "InstanceId": "i-test001",
            "AssociationId": "eipassoc-test001",
            "Domain": "vpc"
        },
        {
            "AllocationId": "eipalloc-test002",
            "PublicIp": "5.6.7.8",
            "PrivateIp": "10.0.0.20",
            "InstanceId": "i-test002",
            "AssociationId": "eipassoc-test002",
            "Domain": "vpc"
        }
    ]

    unassociated = service.get_unassociated_addresses(addresses)

    assert unassociated == []


def test_eip_service_handles_empty_response():

    service, mock_client = create_eip_service()

    mock_response = {
        "Addresses": []
    }

    with patch.object(
        service,
        "get_addresses",
        return_value=mock_response
    ):

        addresses = service.list_addresses()

    assert addresses == []