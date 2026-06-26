import json
import time
from app.services.image_service import download_image
from app.celery_app import celery
from app.core.redis_client import redis_client


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

    # Simulate heavy processing
    local_image = download_image(job["file_name"])

    print(f"Downloaded Image: {local_image}")

    # Update status -> completed
    job["status"] = "completed"
    job["message"] = "Image processed successfully"

    redis_client.set(job_id, json.dumps(job))

    print(f"========== Completed {job_id} ==========")

    return "Success"