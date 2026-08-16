from unittest.mock import MagicMock

from aws.client_factory import AWSClientFactory


def test_client_factory_creates_ec2_client():

    auth = MagicMock()

    mock_session = MagicMock()
    mock_ec2_client = MagicMock()

    # AWSAuth.create_session() ka mock
    auth.create_session.return_value = mock_session

    # session.client("ec2") ka mock
    mock_session.client.return_value = mock_ec2_client

    factory = AWSClientFactory(auth)

    client = factory.get_client("ec2")

    # Client verify
    assert client is mock_ec2_client

    # Session creation verify
    auth.create_session.assert_called_once_with()

    # EC2 client creation verify
    mock_session.client.assert_called_once_with("ec2")


def test_client_factory_creates_client_multiple_times():

    auth = MagicMock()

    mock_session = MagicMock()
    mock_ec2_client = MagicMock()

    auth.create_session.return_value = mock_session
    mock_session.client.return_value = mock_ec2_client

    factory = AWSClientFactory(auth)

    first_client = factory.get_client("ec2")
    second_client = factory.get_client("ec2")

    # Both calls should return the mocked client
    assert first_client is mock_ec2_client
    assert second_client is mock_ec2_client

    # Current AWSClientFactory creates a session
    # whenever get_client() is called.
    assert auth.create_session.call_count == 2

    # Therefore client() is also called twice.
    assert mock_session.client.call_count == 2

    mock_session.client.assert_any_call("ec2")