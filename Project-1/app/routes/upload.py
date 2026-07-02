from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.validation import validate_file_type

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    if not validate_file_type(file.content_type):
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()

    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    return {
        "success": True,
        "filename": file.filename
    }