ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]

def validate_file_type(file_type: str):
    return file_type in ALLOWED_TYPES