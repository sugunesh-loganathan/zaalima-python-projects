from pathlib import Path
import shutil
import uuid

UPLOAD_DIR = Path("app/uploads")

ORIGINAL_DIR = UPLOAD_DIR / "original"
PROCESSED_DIR = UPLOAD_DIR / "processed"

ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def save_original_file(upload_file):

    extension = Path(upload_file.filename).suffix

    unique_filename = f"{uuid.uuid4()}{extension}"

    file_path = ORIGINAL_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return str(file_path)