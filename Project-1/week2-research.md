# Week 2 Research

## Redis

Redis is an open-source in-memory data store used for caching, session storage, and message brokering.

### Why Redis is Used

* High-speed performance
* In-memory storage
* Reduces database load
* Supports caching
* Stores temporary data

## Celery

Celery is a distributed task queue system used for background task processing.

### Why Celery is Used

* Executes tasks asynchronously
* Handles long-running processes
* Supports task scheduling
* Improves application responsiveness

## Background Task Processing

Background task processing allows time-consuming operations to run separately from the main application.

Examples:

* Image resizing
* Video conversion
* File compression
* Data processing

## How Redis and Celery Improve the Project

Redis acts as a message broker between the application and Celery workers.

Celery processes media-related tasks in the background without blocking user requests.

### Workflow

1. User uploads media.
2. Task is sent to Redis.
3. Celery worker receives the task.
4. Media processing is completed.
5. Result is returned to the user.

## Benefits

* Faster response time
* Better scalability
* Improved performance
* Efficient task management
