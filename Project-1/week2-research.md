# Week 2 Research

## Redis Overview

Redis is an open-source in-memory data store used for caching, message brokering, and storing temporary data. It provides high-speed data access and improves application performance.

### Benefits of Redis

* Fast data retrieval
* Reduced database load
* In-memory storage
* Supports caching and queues

## Celery Overview

Celery is a distributed task queue system used for background task processing. It allows long-running tasks to execute asynchronously without blocking the main application.

### Benefits of Celery

* Background processing
* Task scheduling
* Retry failed tasks
* Distributed worker support

## How Redis and Celery Improve Our Project

Our project is a Distributed Media Processing Microservice.

### Current Challenge

Media processing tasks such as image resizing, compression, and conversion may take time and can slow down the application.

### Solution

Redis can act as a message broker and temporary storage system.

Celery can process media tasks in the background.

### Workflow

1. User uploads media.
2. Application sends task to Redis.
3. Celery worker receives task.
4. Media processing is performed in the background.
5. Status is updated and result is returned.

## Advantages

* Faster response time
* Better scalability
* Improved user experience
* Efficient resource utilization
* Reliable task execution
