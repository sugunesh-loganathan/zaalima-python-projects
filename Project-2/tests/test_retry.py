from unittest.mock import patch

import pytest
from botocore.exceptions import ClientError

from utils.retry import aws_retry


def create_client_error(error_code):

    return ClientError(
        {
            "Error": {
                "Code": error_code,
                "Message": "AWS request failed"
            }
        },
        "TestOperation"
    )


def test_retry_succeeds_after_throttling():

    call_count = 0

    @aws_retry(max_retries=3, delay=0)
    def test_function():

        nonlocal call_count

        call_count += 1

        if call_count < 3:
            raise create_client_error("Throttling")

        return "success"

    with patch("utils.retry.time.sleep"):

        result = test_function()

    assert result == "success"
    assert call_count == 3


def test_retry_handles_request_limit_exceeded():

    call_count = 0

    @aws_retry(max_retries=3, delay=0)
    def test_function():

        nonlocal call_count

        call_count += 1

        if call_count < 2:
            raise create_client_error(
                "RequestLimitExceeded"
            )

        return "success"

    with patch("utils.retry.time.sleep"):

        result = test_function()

    assert result == "success"
    assert call_count == 2


def test_retry_raises_after_max_retries():

    call_count = 0

    @aws_retry(max_retries=3, delay=0)
    def test_function():

        nonlocal call_count

        call_count += 1

        raise create_client_error("Throttling")

    with patch("utils.retry.time.sleep"):

        with pytest.raises(ClientError):

            test_function()

    assert call_count == 3


def test_retry_does_not_retry_non_throttling_error():

    call_count = 0

    @aws_retry(max_retries=3, delay=0)
    def test_function():

        nonlocal call_count

        call_count += 1

        raise create_client_error("AccessDenied")

    with pytest.raises(ClientError):

        test_function()

    assert call_count == 1
    