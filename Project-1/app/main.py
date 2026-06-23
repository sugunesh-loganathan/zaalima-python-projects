from fastapi import FastAPI
from app.routes.jobs import router as jobs_router
from app.routes.upload import router as upload_router  
from app.tasks.worker import test_task 

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


@app.get("/test-task")
def run_task():

    task = test_task.delay()

    return {
        "task_id": task.id,
        "message": "Task Sent Successfully"
    }