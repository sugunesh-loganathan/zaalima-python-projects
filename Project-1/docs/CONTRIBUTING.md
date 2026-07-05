# Contributing Guide

Thank you for contributing to the Media Processing Microservice.

This document describes the workflow followed while contributing to the project.

---

# Branch Strategy

Main branches:

- main
- sugunesh-dev
- feature branches

Development should never happen directly on the `main` branch.

---

# Workflow

1. Pull the latest changes.

```bash
git pull origin main
```

2. Create or switch to your development branch.

```bash
git checkout sugunesh-dev
```

3. Create a feature branch if required.

```bash
git checkout -b feature/<feature-name>
```

4. Implement changes.

5. Test the application.

6. Commit using meaningful messages.

Example:

```bash
git commit -m "feat(upload): add image upload endpoint"
```

7. Push changes.

```bash
git push origin feature/<feature-name>
```

8. Create a Pull Request.

9. Review the code.

10. Merge into `main` after approval.

---

# Commit Message Convention

Examples

```
feat(api): add upload endpoint

fix(redis): resolve connection issue

docs: update API documentation

refactor(service): improve job processing

style: format project

test: add celery worker tests
```

---

# Coding Standards

- Follow PEP8
- Use descriptive variable names
- Add comments only where necessary
- Keep functions small and reusable
- Separate business logic from routes
- Store secrets in `.env`

---

# Project Structure

```
app/
    core/
    models/
    routes/
    services/
    tasks/
    utils/
```

Business logic belongs inside the `services` package.

Routes should only handle request validation and responses.

---

# Pull Request Checklist

Before creating a Pull Request:

- Project builds successfully
- No syntax errors
- API tested
- Documentation updated
- No secrets committed
- No unnecessary files added
- Meaningful commit messages

---

# Issue Reporting

When reporting an issue, include:

- Operating System
- Python Version
- Error Logs
- Steps to Reproduce
- Expected Behaviour

---

# Future Contributors

Potential future enhancements include:

- Video Processing
- Authentication
- PostgreSQL
- Docker Compose
- Kubernetes
- Monitoring
- CI/CD Pipeline


---
**Project:** Distributed Media Processing Microservice  
**Organization:** ZAALIMA Internship Program  
**Maintainer:** Sugunesh Loganathan  
**Version:** 1.0.0