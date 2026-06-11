from fastapi import APIRouter, HTTPException
from app.models.response_models import DeleteResponse
from app.utils.constants import IMAGE_DIR, VIDEO_DIR
import os

router = APIRouter(tags=["Delete"])


@router.delete(
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