import time

from app.celery_app import celery
from app.services.job_service import (
    get_job,
    update_job_status,
)


@celery.task(name="app.tasks.worker.process_image")
def process_image(job_id):

    print("=" * 60)
    print("TASK RECEIVED")
    print(f"JOB ID: {job_id}")
    print("=" * 60)

    job = get_job(job_id)

    if not job:
        print("Job not found in Redis!")
        return

    update_job_status(
        job_id,
        status="PROCESSING",
        message="Processing started..."
    )

    print("Processing media...")
    time.sleep(5)

    processed_file = f"processed/{job['file_name']}"

    update_job_status(
        job_id,
        status="COMPLETED",
        message="Processing completed successfully.",
        processed_file=processed_file
    )

    print("Job completed!")

    return {
        "job_id": job_id,
        "status": "COMPLETED"
    }