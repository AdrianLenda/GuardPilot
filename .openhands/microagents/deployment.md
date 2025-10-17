---
name: deployment-guidelines
triggers:
  - docker
  - deployment
  - deploy
  - github
  - ci
  - github-actions
---

# Deployment and Docker Guidelines

## 🐳 Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📦 Docker Compose
- Define services: db, backend, frontend
- Mount volumes for persistence
- Set proper environment variables

## ⚙️ GitHub Actions CI/CD
- Backend workflow: Python, linting, tests
- Frontend workflow: Node.js, linting, tests
- Playwright workflow: E2E tests

## 🚀 Deployment Steps
1. Push to main branch
2. GitHub Actions runs all checks
3. Build Docker images
4. Deploy to production
5. Run smoke tests

## 🔒 Security in Deployment
- Use HTTPS/TLS only
- No sensitive data in images
- Scan images for vulnerabilities
- Don't run as root in containers