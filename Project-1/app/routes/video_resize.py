import os
import subprocess
from fastapi import APIRouter, HTTPException
from app.models.response_models import VideoResizeResponse
from app.utils.constants import VIDEO_DIR

router = APIRouter(tags=["Video Processing"])


@router.post("/video/compress/{filename}", response_model=VideoResizeResponse)
def compress_video(filename: str):

    input_path = os.path.join(VIDEO_DIR, filename)
    output_path = os.path.join(VIDEO_DIR, f"compressed_{filename}")

    print("INPUT:", input_path)
    print("EXISTS:", os.path.exists(input_path))

    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail="Video not found")

    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", input_path,
                "-vf", "scale=1280:720",
                "-crf", "28",
                "-preset", "fast",
                output_path
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=result.stderr
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)

    return VideoResizeResponse(
        message="Video compressed successfully",
        original_file=filename,
        compressed_file=f"compressed_{filename}",
        original_size_mb=round(original_size / (1024 * 1024), 2),
        compressed_size_mb=round(compressed_size / (1024 * 1024), 2),
        reduction_percent=round(((original_size - compressed_size) / original_size) * 100, 2)
    )