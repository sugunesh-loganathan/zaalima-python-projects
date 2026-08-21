from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

from aws.cleanup import CleanupService
from aws.exceptions import AWSCleanupError


def create_test_environment():

    client_factory = MagicMock()

    mock_ec2_client = MagicMock()

    client_factory.get_client.return_value = mock_ec2_client

    cleanup = CleanupService(client_factory)

    cleanup.ebs_service.list_volumes = MagicMock()
    cleanup.eip_service.list_addresses = MagicMock()

    return cleanup, mock_ec2_client


def create_client_error(
    operation,
    code="UnauthorizedOperation",
    message="AWS operation failed"
):

    return ClientError(
        {
            "Error": {
                "Code": code,
                "Message": message
            }
        },
        operation
    )


# ============================================================
# TEST 1 - EBS CLEANUP FAILURE
# ============================================================

def test_ebs_cleanup_handles_aws_failure():

    cleanup, mock_ec2_client = create_test_environment()

    mock_ec2_client.delete_volume.side_effect = create_client_error(
        "DeleteVolume"
    )

    with pytest.raises(AWSCleanupError):

        cleanup.cleanup_volume(
            "vol-test-123",
            dry_run=False
        )


# ============================================================
# TEST 2 - ELASTIC IP CLEANUP FAILURE
# ============================================================

def test_eip_cleanup_handles_aws_failure():

    cleanup, mock_ec2_client = create_test_environment()

    mock_ec2_client.release_address.side_effect = create_client_error(
        "ReleaseAddress"
    )

    with pytest.raises(AWSCleanupError):

        cleanup.cleanup_elastic_ip(
            "eipalloc-test-123",
            dry_run=False
        )


# ============================================================
# TEST 3 - EBS INVALID ID
# ============================================================

def test_ebs_cleanup_invalid_id():

    cleanup, mock_ec2_client = create_test_environment()

    with pytest.raises(
        ValueError,
        match="Volume ID is required."
    ):

        cleanup.cleanup_volume(
            None,
            dry_run=False
        )

    mock_ec2_client.delete_volume.assert_not_called()


# ============================================================
# TEST 4 - EIP INVALID ID
# ============================================================

def test_eip_cleanup_invalid_id():

    cleanup, mock_ec2_client = create_test_environment()

    with pytest.raises(
        ValueError,
        match="Allocation ID is required."
    ):

        cleanup.cleanup_elastic_ip(
            None,
            dry_run=False
        )

    mock_ec2_client.release_address.assert_not_called()


# ============================================================
# TEST 5 - EBS DISCOVERY FAILURE
# ============================================================

def test_workflow_handles_ebs_discovery_failure():

    cleanup, _ = create_test_environment()

    cleanup.ebs_service.list_volumes.side_effect = Exception(
        "EBS discovery failed"
    )

    with pytest.raises(Exception):

        cleanup.run_cleanup_workflow(
            dry_run=True
        )


# ============================================================
# TEST 6 - EIP DISCOVERY FAILURE
# ============================================================

def test_workflow_handles_eip_discovery_failure():

    cleanup, _ = create_test_environment()

    cleanup.ebs_service.list_volumes.return_value = []

    cleanup.eip_service.list_addresses.side_effect = Exception(
        "Elastic IP discovery failed"
    )

    with pytest.raises(Exception):

        cleanup.run_cleanup_workflow(
            dry_run=True
        )


# ============================================================
# TEST 7 - DRY RUN PROTECTS EBS
# ============================================================

def test_dry_run_protects_ebs_after_api_failure():

    cleanup, mock_ec2_client = create_test_environment()

    cleanup.ebs_service.list_volumes.return_value = [
        {
            "VolumeId": "vol-test-123",
            "State": "available",
            "Attachments": 0
        }
    ]

    cleanup.eip_service.list_addresses.return_value = []

    result = cleanup.run_cleanup_workflow(
        dry_run=True
    )

    assert result["status"] == "success"

    assert result["mode"] == "dry_run"

    mock_ec2_client.delete_volume.assert_not_called()


# ============================================================
# TEST 8 - DRY RUN PROTECTS ELASTIC IP
# ============================================================

def test_dry_run_protects_eip_after_api_failure():

    cleanup, mock_ec2_client = create_test_environment()

    cleanup.ebs_service.list_volumes.return_value = []

    cleanup.eip_service.list_addresses.return_value = [
        {
            "AllocationId": "eipalloc-test-123",
            "InstanceId": None
        }
    ]

    result = cleanup.run_cleanup_workflow(
        dry_run=True
    )

    assert result["status"] == "success"

    assert result["mode"] == "dry_run"

    mock_ec2_client.release_address.assert_not_called()