import json
import uuid

from app.core.redis_client import redis_client
from app.core.s3 import generate_presigned_url
from app.tasks.worker import process_image


def create_job(file_name: str, file_type: str, media_type: str):

    job_id = str(uuid.uuid4())

    s3_data = generate_presigned_url(file_name, file_type)

    upload_url = s3_data["upload_url"]
    file_key = s3_data["file_key"]

    job = {
    "job_id": job_id,
    "file_name": file_name,
    "file_key": file_key,
    "media_type": media_type,
    "status": "pending",
    "upload_url": upload_url,
    "processed_file": "",
    "message": ""
}

    redis_client.set(job_id, json.dumps(job))

    return job


def get_job(job_id: str):

    job = redis_client.get(job_id)

    if not job:
        return None

    return json.loads(job)


def start_job(job_id: str):

    job = get_job(job_id)

    if not job:
        return None

    process_image.delay(job_id)

    return job