from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

from aws.pagination import AWSPaginator
from aws.exceptions import AWSAuthenticationError


def test_paginator_success():

    client = MagicMock()

    mock_paginator = MagicMock()

    mock_pages = [
        {
            "Volumes": [
                {"VolumeId": "vol-test-1"}
            ]
        },
        {
            "Volumes": [
                {"VolumeId": "vol-test-2"}
            ]
        }
    ]

    mock_paginator.paginate.return_value = mock_pages

    client.get_paginator.return_value = mock_paginator

    paginator = AWSPaginator(client)

    pages = paginator.paginate("describe_volumes")

    assert pages == mock_pages

    client.get_paginator.assert_called_once_with(
        "describe_volumes"
    )

    mock_paginator.paginate.assert_called_once_with()


def test_paginator_passes_kwargs():

    client = MagicMock()

    mock_paginator = MagicMock()

    mock_pages = [
        {"Instances": []}
    ]

    mock_paginator.paginate.return_value = mock_pages

    client.get_paginator.return_value = mock_paginator

    paginator = AWSPaginator(client)

    pages = paginator.paginate(
        "describe_instances",
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]
    )

    assert pages == mock_pages

    mock_paginator.paginate.assert_called_once_with(
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]
    )


def test_paginator_handles_client_error():

    client = MagicMock()

    error = ClientError(
        {
            "Error": {
                "Code": "AccessDenied",
                "Message": "Access denied"
            }
        },
        "DescribeVolumes"
    )

    client.get_paginator.side_effect = error

    paginator = AWSPaginator(client)

    with pytest.raises(AWSAuthenticationError):

        paginator.paginate("describe_volumes")