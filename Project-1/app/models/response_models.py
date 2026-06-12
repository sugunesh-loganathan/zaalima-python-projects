from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    filename: str
    media_type: str
    content_type: str


class DeleteResponse(BaseModel):
    message: str


class ResizeResponse(BaseModel):
    message: str
    original_file: str
    resized_file: str

    original_size_kb: float
    resized_size_kb: float
    reduction_percent: float

    original_width: int
    original_height: int

    new_width: int
    new_height: int

class VideoResizeResponse(BaseModel):
    message: str

    original_file: str
    compressed_file: str
    thumbnail_file: str

    original_size_mb: float
    compressed_size_mb: float

    reduction_percent: float

    duration_seconds: float

    original_width: int
    original_height: int

    compressed_width: int
    compressed_height: int

    processing_time_seconds: float

    download_url: str