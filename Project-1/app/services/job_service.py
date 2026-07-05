import json
import uuid

from app.core.redis_client import redis_client
from app.core.s3 import generate_presigned_url
from app.celery_app import celery


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
        "status": "PENDING",
        "upload_url": upload_url,
        "processed_file": "",
        "message": ""
    }

    redis_client.set(job_id, json.dumps(job))

    print("\n========== JOB CREATED ==========")
    print(redis_client.get(job_id))

    return job


def get_job(job_id: str):

    print(f"\nReading Job: {job_id}")

    job = redis_client.get(job_id)


    if not job:
        return None

    return json.loads(job)


def update_job_status(
    job_id: str,
    status: str,
    message: str = "",
    processed_file: str = ""
):

    print("\n========== UPDATE JOB ==========")
    print("Job ID :", job_id)
    print("Status :", status)

    job = get_job(job_id)

    if not job:
        print("Job not found in Redis!")
        return


    job["status"] = status
    job["message"] = message

    if processed_file:
        job["processed_file"] = processed_file

    redis_client.set(job_id, json.dumps(job))

    print("After Update:", redis_client.get(job_id))
    


def start_job(job_id: str):

    print("\n========== START JOB ==========")

    job = get_job(job_id)

    if not job:
        print("Job not found!")
        return None

    result = celery.send_task(
        "app.tasks.worker.process_image",
        args=[job_id],
        queue="celery"
    )

    print("Task ID:", result.id)

    return job