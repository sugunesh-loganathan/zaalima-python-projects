import os

IMAGE_DIR = "uploads/images"
VIDEO_DIR = "uploads/videos"

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

ALLOWED_TYPES = [
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp",
    "video/mp4",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-matroska"
]

MAX_FILE_SIZE = 50 * 1024 * 1024