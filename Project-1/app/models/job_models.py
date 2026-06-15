from pydantic import BaseModel

class CreateJobRequest(BaseModel):
    media_type: str
    input_filename: str