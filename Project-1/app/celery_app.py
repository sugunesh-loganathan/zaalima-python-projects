from celery import Celery

celery = Celery(
    "media_processor",
    broker="pyamqp://guest:guest@localhost//",
    backend="rpc://",
    include=["app.tasks.worker"]
)

celery.conf.task_serializer = "json"
celery.conf.accept_content = ["json"]
celery.conf.result_serializer = "json"
celery.conf.timezone = "Asia/Kolkata"
celery.conf.enable_utc = False