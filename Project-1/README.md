# Distributed Media Processing Microservice

## Overview

This project is a scalable backend service developed using FastAPI for asynchronous media processing. It allows users to upload image or video files, create processing jobs, track job status, and process media asynchronously using Celery workers.

The project was developed as part of the ZAALIMA Internship Program.

---

## Features

- Upload images/videos
- Generate secure AWS S3 Pre-Signed URLs
- Asynchronous task processing using Celery
- RabbitMQ as Message Broker
- Redis for Job Status Storage
- Image Processing using Pillow
- RESTful API using FastAPI
- Swagger UI Documentation

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Backend |
| FastAPI | REST API |
| Celery | Background Task Queue |
| RabbitMQ | Message Broker |
| Redis | Job Storage |
| AWS S3 | File Storage |
| Pillow | Image Processing |
| Docker | Containerization |

---

## Folder Structure
Project-1/
│
├── app/
├── uploads/
├── processed/
├── temp/
├── requirements.txt
├── Dockerfile
└── README.md


---

## Project Workflow

1. Upload Media
2. Create Job
3. Generate Upload URL
4. Store Job in Redis
5. Trigger Celery Task
6. Process Image
7. Upload Processed Image
8. Update Job Status

---

## API Endpoints

POST /upload

POST /jobs/create

POST /jobs/start/{job_id}

GET /jobs/status/{job_id}

---

## Author

Sugunesh Loganathan

ZAALIMA Internship
