from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

from aws.cleanup import CleanupService
from aws.exceptions import AWSCleanupError


def create_cleanup_service():

    client_factory = MagicMock()

    mock_ec2_client = MagicMock()

    client_factory.get_client.return_value = mock_ec2_client

    cleanup = CleanupService(client_factory)

    # Mock service methods used by CleanupService
    cleanup.ebs_service.list_volumes = MagicMock()
    cleanup.eip_service.list_addresses = MagicMock()

    return cleanup, mock_ec2_client


# ============================================================
# EBS VALIDATION
# ============================================================

def test_validate_available_unattached_volume():

    cleanup, _ = create_cleanup_service()

    volume = {
        "VolumeId": "vol-test-123",
        "State": "available",
        "Attachments": 0
    }

    assert cleanup.validate_volume(volume) is True


def test_validate_attached_volume():

    cleanup, _ = create_cleanup_service()

    volume = {
        "VolumeId": "vol-test-123",
        "State": "in-use",
        "Attachments": 1
    }

    assert cleanup.validate_volume(volume) is False


# ============================================================
# ELASTIC IP VALIDATION
# ============================================================

def test_validate_unassociated_elastic_ip():

    cleanup, _ = create_cleanup_service()

    address = {
        "AllocationId": "eipalloc-test-123",
        "InstanceId": None
    }

    assert cleanup.validate_elastic_ip(address) is True


def test_validate_associated_elastic_ip():

    cleanup, _ = create_cleanup_service()

    address = {
        "AllocationId": "eipalloc-test-123",
        "InstanceId": "i-test-123"
    }

    assert cleanup.validate_elastic_ip(address) is False


# ============================================================
# EBS DRY RUN
# ============================================================

def test_cleanup_volume_dry_run():

    cleanup, mock_ec2_client = create_cleanup_service()

    result = cleanup.cleanup_volume(
        "vol-test-123",
        dry_run=True
    )

    assert result == {
        "resource_type": "EBS",
        "resource_id": "vol-test-123",
        "action": "delete",
        "dry_run": True,
        "status": "preview"
    }

    mock_ec2_client.delete_volume.assert_not_called()


# ============================================================
# EBS ACTUAL CLEANUP
# ============================================================

def test_cleanup_volume_execute():

    cleanup, mock_ec2_client = create_cleanup_service()

    mock_ec2_client.delete_volume.return_value = {}

    result = cleanup.cleanup_volume(
        "vol-test-123",
        dry_run=False
    )

    assert result == {
        "resource_type": "EBS",
        "resource_id": "vol-test-123",
        "action": "delete",
        "dry_run": False,
        "status": "deleted"
    }

    mock_ec2_client.delete_volume.assert_called_once_with(
        VolumeId="vol-test-123"
    )


# ============================================================
# EBS VALIDATION ERROR
# ============================================================

def test_cleanup_volume_requires_volume_id():

    cleanup, mock_ec2_client = create_cleanup_service()

    with pytest.raises(
        ValueError,
        match="Volume ID is required."
    ):
        cleanup.cleanup_volume(
            None,
            dry_run=True
        )

    mock_ec2_client.delete_volume.assert_not_called()


# ============================================================
# EBS AWS ERROR
# ============================================================

def test_cleanup_volume_handles_aws_error():

    cleanup, mock_ec2_client = create_cleanup_service()

    error = ClientError(
        {
            "Error": {
                "Code": "UnauthorizedOperation",
                "Message": "Not authorized"
            }
        },
        "DeleteVolume"
    )

    mock_ec2_client.delete_volume.side_effect = error

    with pytest.raises(AWSCleanupError) as exc_info:

        cleanup.cleanup_volume(
            "vol-test-123",
            dry_run=False
        )

    assert "UnauthorizedOperation" in str(exc_info.value)


# ============================================================
# ELASTIC IP DRY RUN
# ============================================================

def test_cleanup_elastic_ip_dry_run():

    cleanup, mock_ec2_client = create_cleanup_service()

    result = cleanup.cleanup_elastic_ip(
        "eipalloc-test-123",
        dry_run=True
    )

    assert result == {
        "resource_type": "Elastic IP",
        "resource_id": "eipalloc-test-123",
        "action": "release",
        "dry_run": True,
        "status": "preview"
    }

    mock_ec2_client.release_address.assert_not_called()


# ============================================================
# ELASTIC IP ACTUAL CLEANUP
# ============================================================

def test_cleanup_elastic_ip_execute():

    cleanup, mock_ec2_client = create_cleanup_service()

    mock_ec2_client.release_address.return_value = {}

    result = cleanup.cleanup_elastic_ip(
        "eipalloc-test-123",
        dry_run=False
    )

    assert result == {
        "resource_type": "Elastic IP",
        "resource_id": "eipalloc-test-123",
        "action": "release",
        "dry_run": False,
        "status": "released"
    }

    mock_ec2_client.release_address.assert_called_once_with(
        AllocationId="eipalloc-test-123"
    )


# ============================================================
# ELASTIC IP VALIDATION ERROR
# ============================================================

def test_cleanup_elastic_ip_requires_allocation_id():

    cleanup, mock_ec2_client = create_cleanup_service()

    with pytest.raises(
        ValueError,
        match="Allocation ID is required."
    ):
        cleanup.cleanup_elastic_ip(
            None,
            dry_run=True
        )

    mock_ec2_client.release_address.assert_not_called()


# ============================================================
# ELASTIC IP AWS ERROR
# ============================================================

def test_cleanup_elastic_ip_handles_aws_error():

    cleanup, mock_ec2_client = create_cleanup_service()

    error = ClientError(
        {
            "Error": {
                "Code": "UnauthorizedOperation",
                "Message": "Not authorized"
            }
        },
        "ReleaseAddress"
    )

    mock_ec2_client.release_address.side_effect = error

    with pytest.raises(AWSCleanupError) as exc_info:

        cleanup.cleanup_elastic_ip(
            "eipalloc-test-123",
            dry_run=False
        )

    assert "UnauthorizedOperation" in str(exc_info.value)


# ============================================================
# UNUSED EBS VOLUMES
# ============================================================

def test_get_unused_volumes():

    cleanup, _ = create_cleanup_service()

    cleanup.ebs_service.list_volumes.return_value = [
        {
            "VolumeId": "vol-unused",
            "State": "available",
            "Attachments": 0
        },
        {
            "VolumeId": "vol-used",
            "State": "in-use",
            "Attachments": 1
        }
    ]

    unused = cleanup.get_unused_volumes()

    assert len(unused) == 1
    assert unused[0]["VolumeId"] == "vol-unused"


# ============================================================
# UNUSED ELASTIC IPS
# ============================================================

def test_get_unused_elastic_ips():

    cleanup, _ = create_cleanup_service()

    cleanup.eip_service.list_addresses.return_value = [
        {
            "AllocationId": "eip-unused",
            "InstanceId": None
        },
        {
            "AllocationId": "eip-used",
            "InstanceId": "i-test-123"
        }
    ]

    unused = cleanup.get_unused_elastic_ips()

    assert len(unused) == 1
    assert unused[0]["AllocationId"] == "eip-unused"


# ============================================================
# GENERATE SUMMARY
# ============================================================

def test_generate_summary():

    cleanup, _ = create_cleanup_service()

    cleanup.ebs_service.list_volumes.return_value = [
        {
            "VolumeId": "vol-unused",
            "State": "available",
            "Attachments": 0
        },
        {
            "VolumeId": "vol-used",
            "State": "in-use",
            "Attachments": 1
        }
    ]

    cleanup.eip_service.list_addresses.return_value = [
        {
            "AllocationId": "eip-unused",
            "InstanceId": None
        },
        {
            "AllocationId": "eip-used",
            "InstanceId": "i-test-123"
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

    assert summary["dry_run"] is True


# ============================================================
# DRY RUN WORKFLOW
# ============================================================

def test_cleanup_workflow_dry_run():

    cleanup, mock_ec2_client = create_cleanup_service()

    cleanup.ebs_service.list_volumes.return_value = [
        {
            "VolumeId": "vol-unused",
            "State": "available",
            "Attachments": 0
        }
    ]

    cleanup.eip_service.list_addresses.return_value = [
        {
            "AllocationId": "eip-unused",
            "InstanceId": None
        }
    ]

    result = cleanup.run_cleanup_workflow(
        dry_run=True
    )

    assert result["status"] == "success"
    assert result["mode"] == "dry_run"

    assert result["summary"]["ebs"]["cleanup_candidates"] == 1

    assert (
        result["summary"]["elastic_ips"]["cleanup_candidates"]
        == 1
    )

    mock_ec2_client.delete_volume.assert_not_called()
    mock_ec2_client.release_address.assert_not_called()


# ============================================================
# EXECUTION WORKFLOW
# ============================================================

def test_cleanup_workflow_execute():

    cleanup, mock_ec2_client = create_cleanup_service()

    cleanup.ebs_service.list_volumes.return_value = [
        {
            "VolumeId": "vol-unused",
            "State": "available",
            "Attachments": 0
        }
    ]

    cleanup.eip_service.list_addresses.return_value = [
        {
            "AllocationId": "eip-unused",
            "InstanceId": None
        }
    ]

    mock_ec2_client.delete_volume.return_value = {}

    mock_ec2_client.release_address.return_value = {}

    result = cleanup.run_cleanup_workflow(
        dry_run=False
    )

    assert result["status"] == "success"
    assert result["mode"] == "execute"

    assert len(result["results"]) == 2

    mock_ec2_client.delete_volume.assert_called_once_with(
        VolumeId="vol-unused"
    )

    mock_ec2_client.release_address.assert_called_once_with(
        AllocationId="eip-unused"
    )

def test_dry_run_with_cleanup_candidates():
    cleanup, _ = create_cleanup_service()

    cleanup.ebs_service.list_volumes = lambda: [
        {
            "VolumeId": "vol-unused",
            "State": "available",
            "Attachments": 0
        }
    ]

    cleanup.eip_service.list_addresses = lambda: [
        {
            "AllocationId": "eip-unused",
            "InstanceId": None,
            "PublicIp": "1.2.3.4"
        }
    ]

    result = cleanup.dry_run()

    assert len(result["volumes"]) == 1
    assert result["volumes"][0]["resource_id"] == "vol-unused"

    assert len(result["elastic_ips"]) == 1
    assert result["elastic_ips"][0]["resource_id"] == "eip-unused"

    assert result["volumes"][0]["dry_run"] is True
    assert result["elastic_ips"][0]["dry_run"] is True

def test_dry_run_with_no_cleanup_candidates():
    cleanup, _ = create_cleanup_service()

    cleanup.ebs_service.list_volumes = lambda: []
    cleanup.eip_service.list_addresses = lambda: []

    result = cleanup.dry_run()

    assert result["volumes"] == []
    assert result["elastic_ips"] == []