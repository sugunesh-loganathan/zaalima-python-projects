from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil
import uuid

app = FastAPI(
    title="Media Processing Service",
    description="Image and Video Upload API with Validation",
    version="1.0.0"
)

# ==================================================
# FOLDERS
# ==================================================

IMAGE_DIR = "uploads/images"
VIDEO_DIR = "uploads/videos"

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# ==================================================
# VALIDATION
# ==================================================

ALLOWED_TYPES = [
    # Images
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp",

    # Videos
    "video/mp4",
    "video/quicktime",      # mov
    "video/x-msvideo",      # avi
    "video/x-matroska"      # mkv
]

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

# ==================================================
# PYDANTIC MODELS
# ==================================================

class UploadResponse(BaseModel):
    message: str
    filename: str
    media_type: str
    content_type: str


class DeleteResponse(BaseModel):
    message: str


# ==================================================
# HOME
# ==================================================

@app.get("/")
def home():
    return {
        "message": "Media Processing Service Running Successfully"
    }


# ==================================================
# UPLOAD FILE
# ==================================================

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):

    # File Type Validation
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only image and video files are allowed."
        )

    # Read File
    content = await file.read()

    # File Size Validation
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 50 MB limit."
        )

    # Reset Pointer
    await file.seek(0)

    # Detect Media Type
    if file.content_type.startswith("image"):
        media_type = "image"
        upload_dir = IMAGE_DIR

    elif file.content_type.startswith("video"):
        media_type = "video"
        upload_dir = VIDEO_DIR

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type."
        )

    # Unique Filename
    extension = file.filename.split(".")[-1]

    unique_filename = (
        f"{uuid.uuid4()}.{extension}"
    )

    file_path = os.path.join(
        upload_dir,
        unique_filename
    )

    # Save File
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return UploadResponse(
        message="File uploaded successfully",
        filename=unique_filename,
        media_type=media_type,
        content_type=file.content_type
    )


# ==================================================
# LIST FILES
# ==================================================

@app.get("/files")
def get_files():

    images = os.listdir(IMAGE_DIR)
    videos = os.listdir(VIDEO_DIR)

    return {
        "total_images": len(images),
        "total_videos": len(videos),
        "images": images,
        "videos": videos
    }


# ==================================================
# DELETE FILE
# ==================================================

@app.delete(
    "/files/{media_type}/{filename}",
    response_model=DeleteResponse
)
def delete_file(
    media_type: str,
    filename: str
):

    if media_type == "image":
        file_path = os.path.join(
            IMAGE_DIR,
            filename
        )

    elif media_type == "video":
        file_path = os.path.join(
            VIDEO_DIR,
            filename
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="media_type must be image or video"
        )

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    os.remove(file_path)

    return DeleteResponse(
        message=f"{filename} deleted successfully"
    )