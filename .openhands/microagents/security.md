---
name: security-guidelines
triggers:
  - security
  - auth
  - password
  - token
  - authentication
  - authorization
---

# Security Guidelines

## 🔐 Authentication and Authorization
- **Method**: JWT tokens
- **Token lifetime**: 15 minutes access token
- **Refresh tokens**: 7 days (httpOnly cookie)
- **Storage**: httpOnly cookies (NEVER localStorage!)
- **Password hashing**: Always use bcrypt (min rounds: 12)

## 🛡️ Input Validation
- Validate ALL input data (backend + frontend)
- Use Pydantic on backend
- NEVER trust client-side validation

## 🚫 CRITICAL - NEVER DO
- ❌ Don't commit `.env`, API keys, tokens
- ❌ Don't use SQL injection-prone queries (use ORM)
- ❌ Don't return sensitive data in API
- ❌ Don't log sensitive data
- ❌ Don't deploy with debug=True

## 🌐 API Security
- HTTPS only in production
- CORS - whitelist trusted domains
- Rate limiting on every endpoint
- Error messages - don't reveal details

## 📝 SQL Injection Prevention
- ALWAYS use SQLModel/ORM
- NEVER construct SQL strings with user input

## 🔑 Environment Variables
- Store in `.env` (gitignored)
- Production: AWS Secrets Manager / Azure Key Vault