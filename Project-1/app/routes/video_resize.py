import os
import json
import time
import subprocess

from fastapi import APIRouter, HTTPException

from app.models.response_models import VideoResizeResponse
from app.utils.constants import VIDEO_DIR

router = APIRouter(tags=["Video Processing"])


def get_video_info(video_path: str):

    command = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        "-show_format",
        video_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    data = json.loads(result.stdout)

    video_stream = next(
        stream
        for stream in data["streams"]
        if stream["codec_type"] == "video"
    )

    return {
        "width": video_stream["width"],
        "height": video_stream["height"],
        "duration": float(data["format"]["duration"])
    }


@router.post(
    "/video/compress/{filename}",
    response_model=VideoResizeResponse
)
def compress_video(filename: str):

    input_path = os.path.join(
        VIDEO_DIR,
        filename
    )

    compressed_filename = f"compressed_{filename}"

    output_path = os.path.join(
        VIDEO_DIR,
        compressed_filename
    )

    name, _ = os.path.splitext(filename)

    thumbnail_filename = f"thumb_{name}.jpg"

    thumbnail_path = os.path.join(
        VIDEO_DIR,
        thumbnail_filename
    )

    if not os.path.exists(input_path):
        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    start_time = time.time()

    original_info = get_video_info(input_path)

    original_width = original_info["width"]
    original_height = original_info["height"]
    duration = round(
        original_info["duration"],
        2
    )

    try:

        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                input_path,

                "-vf",
                "scale=1280:-2",

                "-crf",
                "28",

                "-preset",
                "fast",

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

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                input_path,

                "-ss",
                "00:00:01",

                "-vframes",
                "1",

                thumbnail_path
            ],
            capture_output=True,
            text=True
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    compressed_info = get_video_info(
        output_path
    )

    compressed_width = compressed_info["width"]
    compressed_height = compressed_info["height"]

    original_size = os.path.getsize(
        input_path
    )

    compressed_size = os.path.getsize(
        output_path
    )

    processing_time = round(
        time.time() - start_time,
        2
    )

    original_mb = round(
        original_size / (1024 * 1024),
        2
    )

    compressed_mb = round(
        compressed_size / (1024 * 1024),
        2
    )

    reduction_percent = round(
        (
            (original_size - compressed_size)
            / original_size
        ) * 100,
        2
    )

    return VideoResizeResponse(
        message="Video compressed successfully",

        original_file=filename,

        compressed_file=compressed_filename,

        thumbnail_file=thumbnail_filename,

        original_size_mb=original_mb,

        compressed_size_mb=compressed_mb,

        reduction_percent=reduction_percent,

        duration_seconds=duration,

        original_width=original_width,
        original_height=original_height,

        compressed_width=compressed_width,
        compressed_height=compressed_height,

        processing_time_seconds=processing_time,

        download_url=f"/uploads/videos/{compressed_filename}"
    )