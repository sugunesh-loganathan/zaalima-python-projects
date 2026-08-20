# Cloud Infrastructure Auditor & Cost Optimizer

## Project Overview

Project 2 is a Python-based command-line application designed to audit
cloud infrastructure and identify resources that may be unused or
underutilized.

The application is being developed with a modular architecture so that
different AWS services can be scanned independently and their results
can later be used for reporting and cost optimization.

---

## Objectives

The main objectives of the project are:

- Discover AWS cloud resources.
- Analyze resource usage and state.
- Identify potentially unused or underutilized resources.
- Provide recommendations for optimization.
- Generate structured scan results.
- Provide a simple command-line interface for users.
- Build the application using a modular and extensible architecture.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Typer | Command-line interface |
| Boto3 | AWS service integration |
| AWS EC2 | Infrastructure resource discovery |
| AWS CloudWatch | Resource utilization monitoring |
| Logging | Application and scanner logging |
| Git & GitHub | Version control and collaboration |

---

## Project Structure

```text
Project-2/
│
├── app/
│   ├── aws/
│   │   ├── auth.py
│   │   ├── session.py
│   │   └── __init__.py
│   │
│   ├── cli/
│   │   ├── scan.py
│   │   ├── report.py
│   │   ├── cleanup.py
│   │   ├── version.py
│   │   └── __init__.py
│   │
│   ├── config/
│   │   └── ...
│   │
│   ├── models/
│   │   └── scan_result.py
│   │
│   ├── scanner/
│   │   ├── base_scanner.py
│   │   ├── ec2_scanner.py
│   │   ├── ebs_scanner.py
│   │   ├── iam_scanner.py
│   │   ├── s3_scanner.py
│   │   └── ...
│   │
│   ├── utils/
│   │   └── ...
│   │
│   ├── main.py
│   └── __init__.py
│
└── README.md
