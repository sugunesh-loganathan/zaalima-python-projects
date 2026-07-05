# API Documentation

## Base URL

```
http://localhost:8000
```

---

# Upload File

### Endpoint

```
POST /upload
```

### Form Data

| Field | Type |
|--------|------|
| file | File |

### Response

```json
{
    "success": true,
    "filename": "image.jpg"
}
```

---

# Create Job

### Endpoint

```
POST /jobs/create
```

### Request

```json
{
    "media_type":"image",
    "input_filename":"image.jpg"
}
```

### Response

```json
{
    "job_id":"xxxxxxxx",
    "upload_url":"https://..."
}
```

---

# Start Job

### Endpoint

```
POST /jobs/start/{job_id}
```

### Response

```json
{
    "job_id":"xxxx",
    "status":"processing"
}
```

---

# Check Status

### Endpoint

```
GET /jobs/status/{job_id}
```

### Response

```json
{
    "job_id":"xxxx",
    "status":"completed",
    "processed_file":"output.jpg",
    "message":"Success"
}
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
|200|Success|
|400|Bad Request|
|404|Not Found|
|500|Internal Server Error|
