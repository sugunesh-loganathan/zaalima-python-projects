# Week 1 Research

## Redis

### What is Redis?
Redis (Remote Dictionary Server) is an open-source in-memory data store used for caching and storing data.

### Why Redis is Used?
- Fast performance
- In-memory storage
- Job status tracking
- Caching support

### Redis in Our Project
Redis stores the status of media processing jobs:
- Pending
- Processing
- Completed
- Failed

---

## Celery

### What is Celery?
Celery is a distributed task queue used for background task processing.

### Why Celery is Used?
- Asynchronous processing
- Improves application performance
- Supports task retries

### Celery in Our Project
Celery will process:
- Image resizing
- Video compression
- Watermarking

---

## Future Integration

User Uploads File
↓
FastAPI Receives Request
↓
Celery Creates Task
↓
Redis Stores Status
↓
Worker Processes File
↓
Status Updated
↓
Result Returned
