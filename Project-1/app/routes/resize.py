from fastapi import APIRouter, HTTPException
from PIL import Image
from app.models.response_models import ResizeResponse
from app.utils.constants import IMAGE_DIR
import os

router = APIRouter(tags=["Image Processing"])


@router.post("/resize/{filename}", response_model=ResizeResponse)
def resize_image(filename: str):

    image_path = os.path.join(
        IMAGE_DIR,
        filename
    )

    if not os.path.exists(image_path):
        raise HTTPException(
            status_code=404,
            detail="Image not found"
        )

    # Original Size
    original_size = os.path.getsize(image_path)

    image = Image.open(image_path)
    original_width, original_height = image.size

    # Maintain Aspect Ratio
    image.thumbnail((800, 800))
    width, height = image.size

    resized_filename = f"resized_{filename}"

    resized_path = os.path.join(
        IMAGE_DIR,
        resized_filename
    )

    # Better Compression
    image.save(
        resized_path,
        optimize=True,
        quality=70
    )

    # New Size
    resized_size = os.path.getsize(resized_path)

    original_kb = round(original_size / 1024, 2)
    resized_kb = round(resized_size / 1024, 2)

    reduction = round(
        ((original_size - resized_size) / original_size) * 100,
        2
    )

    return ResizeResponse(
    message="Image resized successfully",
    original_file=filename,
    resized_file=resized_filename,

    original_size_kb=original_kb,
    resized_size_kb=resized_kb,
    reduction_percent=reduction,

    original_width=original_width,
    original_height=original_height,

    new_width=width,
    new_height=height
)