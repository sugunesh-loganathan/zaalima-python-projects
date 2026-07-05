# System Architecture

## Overview

The Media Processing Microservice follows a distributed asynchronous architecture. The system separates API handling from media processing, allowing long-running image processing tasks to execute in the background without blocking client requests.

---

# High-Level Architecture

```
                +----------------------+
                |      Client/User     |
                +----------+-----------+
                           |
                    HTTP REST API
                           |
                           v
                +----------------------+
                |       FastAPI        |
                |  API Gateway Layer   |
                +----------+-----------+
                           |
             +-------------+-------------+
             |                           |
             |                           |
             v                           v
     Generate Upload URL          Store Job Metadata
             |                           |
             |                           |
             v                           v
        AWS S3 Bucket               Redis Database
             |
             |
             v
      User Uploads File
             |
             |
             v
      Create Processing Job
             |
             |
             v
        RabbitMQ Queue
             |
             |
             v
      Celery Worker Process
             |
             |
             v
      Image Processing (Pillow)
             |
             |
             v
 Upload Processed Image to S3
             |
             |
             v
     Update Redis Job Status
             |
             |
             v
      Client Polls Job Status
```

---

# Components

## FastAPI

Responsibilities:

- Exposes REST APIs
- Validates incoming requests
- Generates Pre-Signed AWS URLs
- Creates processing jobs
- Returns processing status

---

## AWS S3

Used for:

- Original image uploads
- Processed image storage
- Secure upload using Pre-Signed URLs

---

## Redis

Acts as a lightweight datastore for:

- Job Information
- Processing Status
- File Metadata
- Output File Location

---

## RabbitMQ

Responsible for:

- Queueing image processing requests
- Decoupling API from worker
- Reliable asynchronous messaging

---

## Celery

Handles:

- Background processing
- Task execution
- Worker management

---

## Pillow

Performs:

- Image loading
- Image transformations
- Saving processed images

---

# Processing Flow

1. User uploads image metadata.
2. FastAPI generates a secure AWS S3 upload URL.
3. User uploads the file directly to S3.
4. Client starts processing.
5. FastAPI sends a Celery task.
6. RabbitMQ queues the task.
7. Celery Worker consumes the task.
8. Image is downloaded from S3.
9. Pillow processes the image.
10. Processed image is uploaded back to S3.
11. Redis status is updated.
12. Client retrieves final job status.

---

# Advantages

- Non-blocking API
- Scalable worker architecture
- Secure file uploads
- Distributed task execution
- Easily extensible for video processing

---

# Future Improvements

- Video Processing Support
- PostgreSQL Integration
- JWT Authentication
- Multiple Celery Workers
- Docker Compose Deployment
- Kubernetes Deployment
- Monitoring using Prometheus & Grafana



---
**Project:** Distributed Media Processing Microservice  
**Organization:** ZAALIMA Internship Program  
**Maintainer:** Sugunesh Loganathan  
**Version:** 1.0.0