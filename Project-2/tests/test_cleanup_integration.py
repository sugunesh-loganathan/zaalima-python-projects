from unittest.mock import MagicMock

from aws.cleanup import CleanupService
from aws.client_factory import AWSClientFactory
from aws.auth import AWSAuth


def create_test_environment():

    # Mock AWS authentication
    auth = MagicMock(spec=AWSAuth)

    # Mock AWS session
    auth.create_session.return_value = MagicMock()

    # Create client factory
    factory = AWSClientFactory(auth)

    # Mock EC2 client
    mock_ec2_client = MagicMock()

    # Factory should return our mock client
    factory.get_client = MagicMock(
        return_value=mock_ec2_client
    )

    # Create cleanup service
    cleanup = CleanupService(factory)

    # Mock service methods
    cleanup.ebs_service.list_volumes = MagicMock()
    cleanup.eip_service.list_addresses = MagicMock()

    return cleanup, mock_ec2_client


# ============================================================
# INTEGRATION TEST 1
# EBS + EIP DISCOVERY
# ============================================================

def test_cleanup_discovers_resources():

    cleanup, _ = create_test_environment()

    cleanup.ebs_service.list_volumes.return_value = [
        {
            "VolumeId": "vol-test-001",
            "State": "available",
            "Attachments": 0
        }
    ]

    cleanup.eip_service.list_addresses.return_value = [
        {
            "AllocationId": "eipalloc-test-001",
            "InstanceId": None
        }
    ]

    volumes = cleanup.get_unused_volumes()

    addresses = cleanup.get_unused_elastic_ips()

    assert len(volumes) == 1
    assert volumes[0]["VolumeId"] == "vol-test-001"

    assert len(addresses) == 1
    assert addresses[0]["AllocationId"] == "eipalloc-test-001"


# ============================================================
# INTEGRATION TEST 2
# RESOURCE VALIDATION
# ============================================================

def test_cleanup_validates_resources():

    cleanup, _ = create_test_environment()

    volume = {
        "VolumeId": "vol-test-001",
        "State": "available",
        "Attachments": 0
    }

    address = {
        "AllocationId": "eipalloc-test-001",
        "InstanceId": None
    }

    assert cleanup.validate_volume(volume) is True

    assert cleanup.validate_elastic_ip(address) is True


# ============================================================
# INTEGRATION TEST 3
# CLEANUP CANDIDATES
# ============================================================

def test_cleanup_generates_candidates():

    cleanup, _ = create_test_environment()

    cleanup.ebs_service.list_volumes.return_value = [
        {
            "VolumeId": "vol-test-001",
            "State": "available",
            "Attachments": 0
        },
        {
            "VolumeId": "vol-used-001",
            "State": "in-use",
            "Attachments": 1
        }
    ]

    cleanup.eip_service.list_addresses.return_value = [
        {
            "AllocationId": "eipalloc-test-001",
            "InstanceId": None
        },
        {
            "AllocationId": "eipalloc-used-001",
            "InstanceId": "i-test-001"
        }
    ]

    summary = cleanup.generate_summary(
        dry_run=True
    )

    assert summary["ebs"]["total"] == 2
    assert summary["ebs"]["cleanup_candidates"] == 1

    assert summary["elastic_ips"]["total"] == 2
    assert summary["elastic_ips"]["cleanup_candidates"] == 1

    assert len(summary["recommendations"]) == 2


# ============================================================
# INTEGRATION TEST 4
# DRY RUN WORKFLOW
# ============================================================

def test_complete_dry_run_workflow():

    cleanup, mock_ec2_client = create_test_environment()

    cleanup.ebs_service.list_volumes.return_value = [
        {
            "VolumeId": "vol-test-001",
            "State": "available",
            "Attachments": 0
        }
    ]

    cleanup.eip_service.list_addresses.return_value = [
        {
            "AllocationId": "eipalloc-test-001",
            "InstanceId": None
        }
    ]

    result = cleanup.run_cleanup_workflow(
        dry_run=True
    )

    assert result["status"] == "success"

    assert result["mode"] == "dry_run"

    assert result["summary"]["ebs"]["total"] == 1

    assert (
        result["summary"]["ebs"]["cleanup_candidates"]
        == 1
    )

    assert (
        result["summary"]["elastic_ips"]["cleanup_candidates"]
        == 1
    )

    # Safety check
    mock_ec2_client.delete_volume.assert_not_called()

    mock_ec2_client.release_address.assert_not_called()


# ============================================================
# INTEGRATION TEST 5
# EMPTY AWS ENVIRONMENT
# ============================================================

def test_cleanup_with_no_resources():

    cleanup, mock_ec2_client = create_test_environment()

    cleanup.ebs_service.list_volumes.return_value = []

    cleanup.eip_service.list_addresses.return_value = []

    result = cleanup.run_cleanup_workflow(
        dry_run=True
    )

    assert result["status"] == "success"

    assert result["summary"]["ebs"]["total"] == 0

    assert (
        result["summary"]["ebs"]["cleanup_candidates"]
        == 0
    )

    assert (
        result["summary"]["elastic_ips"]["total"]
        == 0
    )

    assert (
        result["summary"]["elastic_ips"]["cleanup_candidates"]
        == 0
    )

    assert result["summary"]["recommendations"] == []

    mock_ec2_client.delete_volume.assert_not_called()

    mock_ec2_client.release_address.assert_not_called()


# ============================================================
# INTEGRATION TEST 6
# DRY RUN SAFETY
# ============================================================

def test_dry_run_never_modifies_resources():

    cleanup, mock_ec2_client = create_test_environment()

    cleanup.ebs_service.list_volumes.return_value = [
        {
            "VolumeId": "vol-safe-test",
            "State": "available",
            "Attachments": 0
        }
    ]

    cleanup.eip_service.list_addresses.return_value = [
        {
            "AllocationId": "eipalloc-safe-test",
            "InstanceId": None
        }
    ]

    result = cleanup.run_cleanup_workflow(
        dry_run=True
    )

    assert result["mode"] == "dry_run"

    mock_ec2_client.delete_volume.assert_not_called()

    mock_ec2_client.release_address.assert_not_called()

    assert result["summary"]["dry_run"] is True

