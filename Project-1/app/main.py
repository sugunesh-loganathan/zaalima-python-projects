from fastapi import FastAPI

from app.routes.upload import router as upload_router
from app.routes.files import router as files_router
from app.routes.delete import router as delete_router
from app.routes.resize import router as resize_router
from app.routes.jobs import router as jobs_router


app = FastAPI(
    title="Media Processing Service",
    description="Image and Video Upload API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Media Processing Service Running Successfully"
    }


app.include_router(upload_router)
app.include_router(files_router)
app.include_router(delete_router)
app.include_router(resize_router)
app.include_router(jobs_router)
#todais