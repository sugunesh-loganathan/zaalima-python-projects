from celery import Celery
from app.core.config import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
)

celery = Celery(
    "media_processor",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.tasks.worker"]
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=False,
    task_default_queue="celery",
    task_default_exchange="celery",
    task_default_routing_key="celery",
    task_track_started=True,
)