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


def download_media(file_key: str):

    os.makedirs("temp", exist_ok=True)

    file_name = file_key.split("/")[-1]

    local_path = f"temp/{file_name}"

    s3.download_file(
        AWS_BUCKET_NAME,
        file_key,
        local_path
    )

    return local_path

def upload_processed_image(local_path: str, file_name: str):

    s3_key = f"processed/{file_name}"

    s3.upload_file(
        local_path,
        AWS_BUCKET_NAME,
        s3_key
    )

    return f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"