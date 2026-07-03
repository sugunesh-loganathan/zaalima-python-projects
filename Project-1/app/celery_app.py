from celery import Celery

from app.core.config import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND
)

celery = Celery(
    "media_processor",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.tasks.worker"]
)

celery.conf.task_serializer = "json"
celery.conf.accept_content = ["json"]
celery.conf.result_serializer = "json"
celery.conf.timezone = "Asia/Kolkata"
celery.conf.enable_utc = False