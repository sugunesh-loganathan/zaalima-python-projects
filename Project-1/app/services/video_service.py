import os
import subprocess
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

def upload_processed_video(video_path: str, file_name: str):

    s3_key = f"processed/{file_name}"

    s3.upload_file(
        video_path,
        AWS_BUCKET_NAME,
        s3_key
    )

    return f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"

def upload_thumbnail(thumbnail_path: str, file_name: str):

    thumbnail_name = file_name.rsplit(".", 1)[0] + ".jpg"

    s3_key = f"thumbnails/{thumbnail_name}"

    s3.upload_file(
        thumbnail_path,
        AWS_BUCKET_NAME,
        s3_key
    )

    return f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"

def compress_video(input_path: str):

    os.makedirs("processed", exist_ok=True)

    output_path = f"processed/compressed_{os.path.basename(input_path)}"

    command = [
        "ffmpeg",
        "-i", input_path,
        "-vcodec", "libx264",
        "-crf", "28",
        "-preset", "fast",
        "-acodec", "aac",
        output_path,
        "-y"
    ]

    subprocess.run(command, check=True)

    return output_path
def generate_thumbnail(input_path: str):

    os.makedirs("processed", exist_ok=True)

    thumbnail_path = (
        f"processed/{os.path.splitext(os.path.basename(input_path))[0]}.jpg"
    )

    command = [
        "ffmpeg",
        "-i", input_path,
        "-ss", "00:00:01",
        "-vframes", "1",
        thumbnail_path,
        "-y"
    ]

    subprocess.run(command, check=True)

    return thumbnail_path