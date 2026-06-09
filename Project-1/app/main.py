from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil
import uuid

app = FastAPI(
    title="Media Processing Service",
    description="Image Upload API with Validation",
    version="1.0.0"
)

# Upload Folder
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed Image Types
ALLOWED_TYPES = [
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp"
]

# Max File Size = 5 MB
MAX_FILE_SIZE = 5 * 1024 * 1024


# -----------------------------
# Pydantic Models
# -----------------------------

class UploadResponse(BaseModel):
    message: str
    filename: str
    content_type: str


class DeleteResponse(BaseModel):
    message: str


# -----------------------------
# Home Endpoint
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Media Processing Service Running Successfully"
    }


# -----------------------------
# Upload Endpoint
# -----------------------------

@app.post("/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):

    # Validate File Type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, PNG and WEBP files are allowed."
        )

    # Read File Content
    content = await file.read()

    # Validate File Size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 5 MB limit."
        )

    # Reset Pointer
    await file.seek(0)

    # Generate Unique File Name
    extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    # Save File
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return UploadResponse(
        message="File uploaded successfully",
        filename=unique_filename,
        content_type=file.content_type
    )


# -----------------------------
# Get All Uploaded Files
# -----------------------------

@app.get("/files")
def get_files():

    files = os.listdir(UPLOAD_DIR)

    return {
        "total_files": len(files),
        "files": files
    }


# -----------------------------
# Delete File
# -----------------------------

@app.delete(
    "/files/{filename}",
    response_model=DeleteResponse
)
def delete_file(filename: str):

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    os.remove(file_path)

    return DeleteResponse(
        message=f"{filename} deleted successfully."
    )