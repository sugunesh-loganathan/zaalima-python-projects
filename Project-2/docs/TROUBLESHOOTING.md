# Troubleshooting Guide

## Common Issues

### 1. Dependencies Not Installed

If the application does not run because of missing packages, install the required dependencies:

```bash
pip install -r requirements.txt

### 2. Python Command Not Found

Make sure Python is installed and added to the system PATH.

Check the Python installation using:

```bash
python --version

### 3. Application Does Not Start

Make sure you are running the command from the Project-2 directory:

```bash
python app/main.py

### 4. Environment Configuration

If the project requires environment variables, create a `.env` file based on `.env.example` and configure the required values.

### 5. Virtual Environment

It is recommended to use a Python virtual environment to avoid dependency conflicts.

## Notes

If an issue still occurs, check the error message in the terminal and verify that all required dependencies and configurations are properly set.
