from fastapi import APIRouter
from app.utils.constants import IMAGE_DIR, VIDEO_DIR
import os

router = APIRouter(tags=["Files"])


@router.get("/files")
def get_files():

    images = os.listdir(IMAGE_DIR)
    videos = os.listdir(VIDEO_DIR)

    return {
        "total_images": len(images),
        "total_videos": len(videos),
        "images": images,
        "videos": videos
    }