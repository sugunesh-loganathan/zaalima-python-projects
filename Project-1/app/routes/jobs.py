import uuid
import os

from fastapi import APIRouter
from app.models.job_models import (
    CreateJobRequest,
    CreateJobResponse
)

from app.services.s3_service import s3_client

router = APIRouter(tags=["Jobs"])

@router.post(
    "/jobs",
    response_model=CreateJobResponse
)
def create_job(request: CreateJobRequest):

    job_id = str(uuid.uuid4())

    s3_key = f"uploads/{job_id}_{request.input_filename}"

    upload_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": os.getenv("AWS_BUCKET_NAME"),
            "Key": s3_key
        },
        ExpiresIn=3600
    )

    return CreateJobResponse(
        job_id=job_id,
        upload_url=upload_url
    )