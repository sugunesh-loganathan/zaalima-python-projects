import json
import time
from app.celery_app import celery
from app.core.redis_client import redis_client

from app.services.processing_service import (
    resize_image,
    delete_file
)

from app.services.image_service import (
    download_media,
    upload_processed_image
)

from app.services.video_service import (
    compress_video,
    generate_thumbnail,
    upload_processed_video,
    upload_thumbnail
)


@celery.task(name="app.tasks.worker.process_image")
def process_image(job_id: str):

    job = redis_client.get(job_id)

    if not job:
        return "Job not found"

    job = json.loads(job)

    try:

        print(f"========== Processing {job_id} ==========")

        # Update status -> processing
        job["status"] = "processing"
        redis_client.set(job_id, json.dumps(job))
        
        print("Job Data:", job)
        print("File Key:", job["file_key"])

        # Download original file from S3
        local_file = download_media(job["file_key"])

        print(f"Downloaded File: {local_file}")

        # ==========================
        # IMAGE PROCESSING
        # ==========================
        if job["media_type"] == "image":

            processed_file = resize_image(local_file)

            processed_url = upload_processed_image(
                processed_file,
                job["file_name"]
            )

            job["processed_file"] = processed_url
            job["message"] = "Image processed successfully"

        # ==========================
        # VIDEO PROCESSING
        # ==========================
        elif job["media_type"] == "video":

            processed_file = compress_video(local_file)

            thumbnail = generate_thumbnail(local_file)

            processed_url = upload_processed_video(
                processed_file,
                job["file_name"]
            )

            thumbnail_url = upload_thumbnail(
                thumbnail,
                job["file_name"]
            )

            job["processed_file"] = processed_url
            job["thumbnail"] = thumbnail_url
            job["message"] = "Video processed successfully"

        else:
            raise Exception("Unsupported media type")

        # Update status
        job["status"] = "completed"
        redis_client.set(job_id, json.dumps(job))

        # Cleanup local files
        delete_file(local_file)
        delete_file(processed_file)

        if job["media_type"] == "video":
            delete_file(thumbnail)

        print(f"========== Completed {job_id} ==========")

        return "Success"

    except Exception as e:

        job["status"] = "failed"
        job["message"] = str(e)

        redis_client.set(job_id, json.dumps(job))

        print(f"ERROR: {e}")

        return "Failed"