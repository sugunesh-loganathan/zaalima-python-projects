from fastapi import FastAPI, UploadFile, File
from app.utils.storage import save_file

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server Running"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    saved_path = save_file(file)

    return {
        "message": "File uploaded successfully",
        "path": saved_path
    }