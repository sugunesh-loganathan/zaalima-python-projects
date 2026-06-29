import uuid
import boto3
from app.core.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    AWS_BUCKET_NAME
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


def generate_presigned_url(file_name: str, file_type: str):

    file_key = f"uploads/{uuid.uuid4()}_{file_name}"

    url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": AWS_BUCKET_NAME,
            "Key": file_key,
            "ContentType": file_type
        },
        ExpiresIn=3600
    )

    return {
        "upload_url": url,
        "file_key": file_key
    }