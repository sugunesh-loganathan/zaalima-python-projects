import json
import time
from app.celery_app import celery
from app.core.redis_client import redis_client

from app.services.image_service import download_image
from app.services.processing_service import resize_image


@celery.task(name="app.tasks.worker.process_image")
def process_image(job_id: str):

    job = redis_client.get(job_id)

    if not job:
        return "Job not found"

    job = json.loads(job)

    print(f"========== Processing {job_id} ==========")

    # Update status -> processing
    job["status"] = "processing"
    redis_client.set(job_id, json.dumps(job))

    # Download image from S3
    local_image = download_image(job["file_key"])

    print(f"Downloaded Image: {local_image}")

    # Resize & Compress Image
    processed_image = resize_image(local_image)

    print(f"Processed Image: {processed_image}")

    # Update status -> completed
    job["status"] = "completed"
    job["message"] = "Image processed successfully"

    redis_client.set(job_id, json.dumps(job))

    print(f"========== Completed {job_id} ==========")

    return "Success"