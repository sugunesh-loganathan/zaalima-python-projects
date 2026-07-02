from fastapi import FastAPI

from app.routes.jobs import router as jobs_router
from app.routes.upload import router as upload_router

app = FastAPI(
    title="Media Processing Service",
    description="Image and Video Upload API",
    version="1.0.0"
)

app.include_router(jobs_router)
app.include_router(upload_router)


@app.get("/")
def home():
    return {"message": "server running"}