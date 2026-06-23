import time
from app.celery_app import celery


@celery.task(name="app.tasks.worker.test_task")
def test_task():

    print("========== TASK STARTED ==========")

    time.sleep(5)

    print("========== TASK COMPLETED ==========")

    return "Success"