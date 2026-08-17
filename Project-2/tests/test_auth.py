from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    ClientError,
    ProfileNotFound
)

from aws.auth import AWSAuth
from aws.exceptions import AWSAuthenticationError


# ============================================================
# TEST 1 - EXISTING SESSION REUSE
# ============================================================

def test_aws_session_reuse():

    auth = AWSAuth(
        profile_name="default",
        region_name="ap-south-1"
    )

    existing_session = MagicMock()

    auth.session = existing_session

    session = auth.create_session()

    assert session is existing_session


# ============================================================
# TEST 2 - PROFILE NOT FOUND
# ============================================================

@patch("aws.auth.boto3.Session")
def test_aws_session_profile_not_found(mock_session):

    mock_session.side_effect = ProfileNotFound(
        profile="invalid-profile"
    )

    auth = AWSAuth(
        profile_name="invalid-profile",
        region_name="ap-south-1"
    )

    with pytest.raises(
        AWSAuthenticationError,
        match="AWS profile not found"
    ):
        auth.create_session()


# ============================================================
# TEST 3 - SESSION CREATION UNEXPECTED ERROR
# ============================================================

@patch("aws.auth.boto3.Session")
def test_aws_session_unexpected_error(mock_session):

    mock_session.side_effect = Exception(
        "Unexpected AWS error"
    )

    auth = AWSAuth(
        profile_name="default",
        region_name="ap-south-1"
    )

    with pytest.raises(
        AWSAuthenticationError,
        match="Unexpected AWS error"
    ):
        auth.create_session()


# ============================================================
# TEST 4 - NO AWS CREDENTIALS
# ============================================================

def test_validate_credentials_no_credentials():

    auth = AWSAuth(
        profile_name="default",
        region_name="ap-south-1"
    )

    mock_session = MagicMock()

    mock_sts = MagicMock()

    mock_sts.get_caller_identity.side_effect = (
        NoCredentialsError()
    )

    mock_session.client.return_value = mock_sts

    auth.session = mock_session

    with pytest.raises(
        AWSAuthenticationError,
        match="AWS credentials not found"
    ):
        auth.validate_credentials()


# ============================================================
# TEST 5 - PARTIAL AWS CREDENTIALS
# ============================================================

def test_validate_credentials_partial_credentials():

    auth = AWSAuth(
        profile_name="default",
        region_name="ap-south-1"
    )

    mock_session = MagicMock()

    mock_sts = MagicMock()

    mock_sts.get_caller_identity.side_effect = (
        PartialCredentialsError(
            provider="aws",
            cred_var="AWS_SECRET_ACCESS_KEY"
        )
    )

    mock_session.client.return_value = mock_sts

    auth.session = mock_session

    with pytest.raises(
        AWSAuthenticationError,
        match="Incomplete AWS credentials"
    ):
        auth.validate_credentials()


# ============================================================
# TEST 6 - PROFILE NOT FOUND DURING VALIDATION
# ============================================================

def test_validate_credentials_profile_not_found():

    auth = AWSAuth(
        profile_name="invalid-profile",
        region_name="ap-south-1"
    )

    mock_session = MagicMock()

    mock_session.client.side_effect = ProfileNotFound(
        profile="invalid-profile"
    )

    auth.session = mock_session

    with pytest.raises(
        AWSAuthenticationError,
        match="AWS profile not found"
    ):
        auth.validate_credentials()


# ============================================================
# TEST 7 - AWS CLIENT ERROR
# ============================================================

def test_validate_credentials_client_error():

    auth = AWSAuth(
        profile_name="default",
        region_name="ap-south-1"
    )

    mock_session = MagicMock()

    mock_sts = MagicMock()

    error = ClientError(
        {
            "Error": {
                "Code": "AccessDenied",
                "Message": "Access denied"
            }
        },
        "GetCallerIdentity"
    )

    mock_sts.get_caller_identity.side_effect = error

    mock_session.client.return_value = mock_sts

    auth.session = mock_session

    with pytest.raises(AWSAuthenticationError):

        auth.validate_credentials()


# ============================================================
# TEST 8 - UNEXPECTED VALIDATION ERROR
# ============================================================

def test_validate_credentials_unexpected_error():

    auth = AWSAuth(
        profile_name="default",
        region_name="ap-south-1"
    )

    mock_session = MagicMock()

    mock_sts = MagicMock()

    mock_sts.get_caller_identity.side_effect = Exception(
        "Unexpected validation error"
    )

    mock_session.client.return_value = mock_sts

    auth.session = mock_session

    with pytest.raises(
        AWSAuthenticationError,
        match="Unexpected validation error"
    ):
        auth.validate_credentials()


# ============================================================
# TEST 9 - VALIDATE CREDENTIALS SUCCESS
# ============================================================

def test_validate_credentials_success():

    auth = AWSAuth(
        profile_name="default",
        region_name="ap-south-1"
    )

    mock_session = MagicMock()

    mock_sts = MagicMock()

    identity = {
        "UserId": "test-user",
        "Account": "123456789",
        "Arn": "arn:aws:iam::123456789:user/test"
    }

    mock_sts.get_caller_identity.return_value = identity

    mock_session.client.return_value = mock_sts

    auth.session = mock_session

    result = auth.validate_credentials()

    assert result == identity

    mock_session.client.assert_called_once_with("sts")

    mock_sts.get_caller_identity.assert_called_once()