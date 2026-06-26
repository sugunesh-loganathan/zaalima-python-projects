import os
import boto3

from app.core.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    AWS_BUCKET_NAME
)

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


def download_image(file_name: str):

    os.makedirs("temp", exist_ok=True)

    local_path = f"temp/{file_name}"

    s3.download_file(
        AWS_BUCKET_NAME,
        f"uploads/{file_name}",
        local_path
    )

    return local_path