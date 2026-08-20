# AWS Scanner Architecture

## Overview

The AWS Scanner is designed to scan different AWS resources and collect standardized information. Each AWS resource has its own scanner, while a common base scanner provides shared functionality.

The scanner architecture is modular, making it easy to add new resource scanners in the future.

---

## Architecture Diagram

AWS Account
│
├── EC2 Scanner
├── EBS Scanner
├── Elastic IP Scanner
└── CloudWatch Scanner

↓

Scanner Base

↓

Standardized Scan Results

↓

Cleanup Recommendation Engine

---

## Components

### Base Scanner

The Base Scanner provides common functionality such as:

- AWS session creation
- Error handling
- Logging
- Standard response format

---

### EC2 Scanner

Responsible for scanning EC2 instances and collecting:

- Instance ID
- State
- Instance Type
- Public IP
- Tags

---

### EBS Scanner

Responsible for scanning EBS volumes and collecting:

- Volume ID
- Size
- State
- Encryption
- Attached Instance

---

### Elastic IP Scanner

Responsible for scanning Elastic IP addresses and collecting:

- Allocation ID
- Public IP
- Association
- Tags

---

### CloudWatch Scanner

Responsible for retrieving utilization metrics such as:

- CPU Utilization
- Network In
- Network Out
- Disk Read
- Disk Write

---

## Standard Scan Result

Each scanner should return results in a common format.

Example:

{
    "resource_type": "",
    "resource_id": "",
    "status": "",
    "region": "",
    "details": {}
}

---

## Benefits

- Modular design
- Easy to maintain
- Easy to extend
- Reusable components
- Standardized output