# Deployment Guide

## Requirements

- Python 3.11+
- Redis
- RabbitMQ
- Docker Desktop
- AWS Account

---

## Clone Repository

```bash
git clone <repository-url>
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create

```
.env
```

Example

```env
AWS_ACCESS_KEY=xxxxxxxx
AWS_SECRET_KEY=xxxxxxxx
AWS_BUCKET_NAME=xxxxxxxx

REDIS_HOST=localhost
REDIS_PORT=6379

CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
CELERY_RESULT_BACKEND=rpc://
```

---

## Start Redis

```bash
Memurai
```

or

```bash
redis-server
```

---

## Start RabbitMQ

```bash
docker run -d \
--name rabbitmq \
-p 5672:5672 \
-p 15672:15672 \
rabbitmq:3-management
```

---

## Run FastAPI

```bash
uvicorn app.main:app --reload
```

---

## Run Celery

```bash
celery -A app.celery_app worker --loglevel=info
```

---

## Open Swagger

```
http://127.0.0.1:8000/docs
```
