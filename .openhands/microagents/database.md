---
name: database-guidelines
triggers:
  - database
  - postgres
  - migration
  - alembic
  - sqlmodel
---

# Database Guidelines

## 🗄️ PostgreSQL (Production)
- **Version**: PostgreSQL 14+
- **Connection**: psycopg2-binary
- **Migrations**: Alembic

## 📝 Model Definitions
- All models in `backend/app/models.py`
- Define all fields with proper types
- Add indexes for frequently-queried columns

## 🔄 Migrations (Alembic)
```bash
alembic revision --autogenerate -m "Add user table"
alembic upgrade head
alembic downgrade -1
```

## 📊 Indexes
- Index on unique fields (email, username)
- Index on frequently-queried columns
- Index on foreign keys
- Avoid over-indexing

## 🔗 Relationships
- Define relationships in models
- Use Relationship() for SQLModel

## ⚠️ Query Optimization
- Use eager loading for relationships
- Add pagination for list endpoints