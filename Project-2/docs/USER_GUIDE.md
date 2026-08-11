# Project-2 User Guide

## Overview

Project-2 is a command-line application for cloud infrastructure-related operations.

## Prerequisites

Before using Project-2, make sure the following are installed:

- Python
- Git
- Docker, if required by the project

## Installation

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

## Running the Application

Open a terminal in the Project-2 directory and run:

```bash
python app/main.py
```

## Using the Application

Project-2 provides a command-line interface (CLI) for interacting with the application.

Currently, the application provides a basic command for initializing the CLI.

## Example Command

Run the application using:

```bash
python app/main.py
```

The application will initialize the Project-2 CLI.

### Example Output

When the application starts successfully, it displays:

```text
Cloud Infrastructure Auditor CLI Initialized
```

### Command Summary

| Command | Purpose |
|---|---|
| `python app/main.py` | Starts the Project-2 CLI application |
| `python --version` | Checks the installed Python version |
| `pip install -r requirements.txt` | Installs the required project dependencies |

## Troubleshooting

If the application does not start:

- Check that Python is installed.
- Make sure the required dependencies are installed.
- Make sure you are running the command from the Project-2 directory.
- Check the required environment configuration.

For more troubleshooting information, refer to `TROUBLESHOOTING.md`.

## Related Documentation

- `ARCHITECTURE.md` – Project architecture and folder structure.
- `DOCUMENTATION.md` – Technical documentation.
- `CONTRIBUTING.md` – Contribution guidelines.
- `TROUBLESHOOTING.md` – Common issues and solutions.
