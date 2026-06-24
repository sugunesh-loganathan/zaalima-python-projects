import uuid

from app.models.job_store import jobs
from app.core.s3 import generate_presigned_url
from app.tasks.worker import process_image


def create_job(file_name: str, file_type: str):

    job_id = str(uuid.uuid4())

    upload_url = generate_presigned_url(file_name, file_type)

    jobs[job_id] = {
        "job_id": job_id,
        "file_name": file_name,
        "status": "pending",
        "upload_url": upload_url,
        "processed_file": None,
        "message": ""
    }

    return jobs[job_id]


def get_job(job_id: str):
    return jobs.get(job_id)


def start_job(job_id: str):

    job = jobs.get(job_id)

    if not job:
        return None

    process_image.delay(job_id)

    return job