import os
import uuid

from fastapi import APIRouter, HTTPException

from app.models.response_models import (
    CreateJobRequest,
    CreateJobResponse
)

from app.services.s3_service import (
    s3_client,
    BUCKET_NAME
)

router = APIRouter(
    tags=["Job Processing"]
)


@router.post(
    "/jobs/create",
    response_model=CreateJobResponse
)
def create_job(
    request: CreateJobRequest
):

    try:

        job_id = str(uuid.uuid4())

        s3_key = (
            f"uploads/{job_id}_{request.input_filename}"
        )

        upload_url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": s3_key
            },
            ExpiresIn=3600
        )

        return CreateJobResponse(
            job_id=job_id,
            upload_url=upload_url
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )