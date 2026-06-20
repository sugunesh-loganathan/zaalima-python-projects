from fastapi import FastAPI
from app.routes.jobs import router as jobs_router
from app.routes.upload import router as upload_router   

app = FastAPI()

app.include_router(jobs_router)
app.include_router(upload_router)   

@app.get("/")
def home():
    return {"message": "server running"}