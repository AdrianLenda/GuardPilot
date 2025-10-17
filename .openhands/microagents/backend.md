---
name: backend-guidelines
triggers:
  - backend
  - python
  - fastapi
  - sqlmodel
---

# Backend Development Guidelines

## 🐍 Python Standards
- **Python version**: 3.11+
- **Type hints**: MANDATORY for every function
- **Docstrings**: Every public function must have a docstring
- **Linting**: ruff, black, mypy

## 🗄️ Database and SQLModel
- All models in `app/models.py`
- Use SQLModel for models (ORM + Pydantic validation)
- Migrations: Alembic

## 🔌 API Endpoints
- REST conventions (GET, POST, PUT, DELETE)
- Type hints for request/response
- Error handling with appropriate HTTP codes

## ✅ Testing (pytest)
- Location: `backend/tests/`
- Naming: `test_*.py`
- Each function/endpoint must have a test

## 📦 Dependencies
- Minimize external dependencies
- Always pin versions in requirements.txt

## ⚠️ Anti-patterns to Avoid
- ❌ Global variables/state
- ❌ Synchronous code in async context
- ❌ Missing error handling