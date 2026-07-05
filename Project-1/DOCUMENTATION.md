# Project 1 - Distributed Media Processing Microservice

## Overview

The Distributed Media Processing Microservice is designed to process image and video files asynchronously using a distributed architecture.

Instead of processing uploaded media directly within the API server, the application delegates processing tasks to background workers through a message queue. This improves scalability, responsiveness, and reliability.

---

# Objectives

* Upload media files securely to AWS S3.
* Generate secure pre-signed upload URLs.
* Process images asynchronously.
* Process videos asynchronously.
* Track processing status.
* Build a scalable microservice architecture using FastAPI, Redis, RabbitMQ, and Celery.

---

# Technology Stack

| Component            | Technology           |
| -------------------- | -------------------- |
| Backend Framework    | FastAPI              |
| Programming Language | Python 3.11          |
| Background Workers   | Celery               |
| Message Broker       | RabbitMQ             |
| Job Storage          | Redis                |
| Cloud Storage        | AWS S3               |
| Image Processing     | Pillow               |
| Video Processing     | FFmpeg               |
| Configuration        | python-dotenv        |
| API Documentation    | Swagger UI (OpenAPI) |

---

# Project Architecture

```text
                Client
                   │
                   ▼
            FastAPI Server
                   │
      Generate Pre-Signed URL
                   │
                   ▼
               AWS S3 Upload
                   │
                   ▼
          Create Processing Job
                   │
             Store Job (Redis)
                   │
                   ▼
        Send Task (RabbitMQ)
                   │
                   ▼
           Celery Worker
         ┌─────────┴─────────┐
         │                   │
         ▼                   ▼
 Image Processing     Video Processing
   (Pillow)              (FFmpeg)
         │                   │
         └─────────┬─────────┘
                   ▼
        Upload Processed File
               AWS S3
                   │
                   ▼
      Update Job Status (Redis)
```

---

# Folder Structure

```text
Project-1/
│
├── app/
│   ├── core/
│   ├── routes/
│   ├── services/
│   ├── tasks/
│   ├── utils/
│   ├── main.py
│   └── celery_app.py
│
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

---

# Workflow

## Step 1 – Upload Media

The client uploads an image or video using the Upload API.

The server stores the uploaded media in AWS S3.

---

## Step 2 – Create Job

The client creates a processing job by providing:

* Media Type
* File Name

The server:

* Generates a unique Job ID
* Creates a Redis job entry
* Returns a secure upload URL

---

## Step 3 – Start Processing

The client starts the processing job.

FastAPI sends a Celery task to RabbitMQ.

---

## Step 4 – Worker Execution

Celery workers receive the task from RabbitMQ.

Depending on the media type:

### Image

* Download original image
* Resize using Pillow
* Upload processed image to AWS S3

### Video

* Download original video
* Compress using FFmpeg
* Generate thumbnail
* Upload processed video
* Upload thumbnail

---

## Step 5 – Update Status

After successful processing:

Redis updates:

* Status
* Processed File URL
* Thumbnail URL (videos)
* Success message

If processing fails:

* Status becomes Failed
* Error message is stored

---

# API Endpoints

## Upload API

POST

```
/upload
```

Uploads media to AWS S3.

---

## Create Job

POST

```
/jobs/create
```

Creates a new processing job.

---

## Start Job

POST

```
/jobs/start/{job_id}
```

Sends the processing task to Celery.

---

## Job Status

GET

```
/jobs/status/{job_id}
```

Returns the current job status.

---

# Job Lifecycle

```text
Pending
   │
   ▼
Processing
   │
   ├────► Failed
   │
   ▼
Completed
```

---

# Environment Variables

Required environment variables:

```
AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_REGION

AWS_BUCKET_NAME

REDIS_HOST

REDIS_PORT

CELERY_BROKER_URL

CELERY_RESULT_BACKEND
```

---

# Key Features

* Secure AWS S3 uploads
* Asynchronous background processing
* Distributed task execution
* Redis job tracking
* RabbitMQ message queuing
* Image resizing
* Video compression
* Thumbnail generation
* RESTful APIs
* Swagger API documentation

---

# Error Handling

The application handles:

* Unsupported media types
* Invalid requests
* Missing jobs
* AWS upload failures
* Redis failures
* Worker exceptions
* Processing failures

Job status is automatically updated when an error occurs.

---

# Scalability

The architecture supports horizontal scaling.

Additional Celery workers can be started without modifying the API server.

RabbitMQ distributes tasks across available workers, enabling concurrent processing of multiple jobs.

---

# Future Improvements

* Docker Compose deployment
* Prometheus monitoring
* Grafana dashboards
* Automatic retries
* JWT authentication
* Rate limiting
* Kubernetes deployment
* CI/CD pipeline
* Object versioning
* Multi-worker auto scaling

---

# Developed By

Project developed as part of the Distributed Media Processing Microservice internship project using FastAPI, Redis, RabbitMQ, Celery, AWS S3, Pillow, and FFmpeg.
