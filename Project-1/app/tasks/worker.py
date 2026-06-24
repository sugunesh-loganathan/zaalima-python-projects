import time

from app.celery_app import celery
from app.models.job_store import jobs


@celery.task(name="app.tasks.worker.process_image")
def process_image(job_id: str):

    job = jobs.get(job_id)

    if not job:
        return "Job not found"

    print(f"Processing Job : {job_id}")

    job["status"] = "processing"

    # Temporary processing simulation
    time.sleep(5)

    job["status"] = "completed"
    job["message"] = "Image processed successfully"

    print(f"Completed Job : {job_id}")

    return "Success"