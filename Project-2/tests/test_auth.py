import boto3

from moto import mock_aws

from aws.auth import AWSAuth


@mock_aws
def test_aws_session_creation():

    auth = AWSAuth(
        profile_name=None,
        region_name="ap-south-1"
    )

    session = auth.create_session()

    assert session is not None
    assert session.region_name == "ap-south-1"


@mock_aws
def test_aws_credentials_validation():

    auth = AWSAuth(
        profile_name=None,
        region_name="ap-south-1"
    )

    auth.create_session()

    identity = auth.validate_credentials()

    assert identity is not None
    assert "Account" in identity
    assert "Arn" in identity
    assert "UserId" in identity