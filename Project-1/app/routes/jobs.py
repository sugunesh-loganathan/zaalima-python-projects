from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.job_service import create_job, get_job, start_job
from app.utils.validation import validate_file_type


router = APIRouter()

class JobRequest(BaseModel):
    media_type: str
    input_filename: str


@router.post("/jobs/create")
def create_jobs(req: JobRequest):

    file_type = "image/jpeg"  # simplified (frontend can send actual type)

    if not validate_file_type(file_type):
        raise HTTPException(status_code=400, detail="Invalid file type")

    job = create_job(req.input_filename, file_type)

    return {
        "job_id": job["job_id"],
        "upload_url": job["upload_url"]
    }


@router.get("/jobs/status/{job_id}")
def job_status(job_id: str):

    job = get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
    "job_id": job_id,
    "status": job["status"],
    "processed_file": job["processed_file"],
    "message": job["message"]
    }

@router.post("/jobs/start/{job_id}")
def start_processing(job_id: str):

    job = start_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "message": "Processing Started",
        "job_id": job_id
    }