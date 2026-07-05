# Troubleshooting Guide

## Redis Module Not Found

### Error

```
ModuleNotFoundError: redis
```

### Solution

```bash
pip install redis
```

---

## Redis Not Running

### Error

```
Connection refused
```

### Solution

Start Memurai or Redis server.

---

## RabbitMQ Not Starting

### Cause

Incompatible Erlang Version

### Solution

Use Docker RabbitMQ image.

---

## Docker Engine Stopped

### Cause

Virtualization Disabled

### Solution

Enable Virtualization in BIOS and start Docker Desktop.

---

## Celery Task Not Executing

### Verify

```bash
celery -A app.celery_app inspect registered
```

Should show

```
app.tasks.worker.process_image
```

---

## AWS Upload Failure

### Verify

- Bucket Name
- Region
- IAM Permissions
- AWS Keys

---

## Job Always Pending

### Check

- Redis Running
- RabbitMQ Running
- Celery Worker Running
- Task Registered

---

## Swagger Not Updating

Restart FastAPI

```bash
CTRL + C

uvicorn app.main:app --reload
```

---

## Common Commands

FastAPI

```bash
uvicorn app.main:app --reload
```

Celery

```bash
celery -A app.celery_app worker --loglevel=info
```

RabbitMQ

```bash
docker ps
```

Redis

```bash
Get-Service Memurai
```
