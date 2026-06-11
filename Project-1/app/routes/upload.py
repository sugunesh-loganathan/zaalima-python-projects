from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.response_models import UploadResponse
from app.utils.constants import (
    ALLOWED_TYPES,
    MAX_FILE_SIZE,
    IMAGE_DIR,
    VIDEO_DIR
)

import uuid
import os
import shutil

router = APIRouter(tags=["Upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only image and video files are allowed."
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 50 MB limit."
        )

    await file.seek(0)

    if file.content_type.startswith("image"):
        media_type = "image"
        upload_dir = IMAGE_DIR

    elif file.content_type.startswith("video"):
        media_type = "video"
        upload_dir = VIDEO_DIR

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported media type."
        )

    extension = file.filename.split(".")[-1]

    unique_filename = f"{uuid.uuid4()}.{extension}"

    file_path = os.path.join(
        upload_dir,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return UploadResponse(
        message="File uploaded successfully",
        filename=unique_filename,
        media_type=media_type,
        content_type=file.content_type
    )