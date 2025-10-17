---
name: orchestrator-guidelines
triggers:
  - orchestrate
  - coordinate
  - integrate
  - feature
  - workflow
---

# Orchestrator - Cross-Component Coordination

## 🎼 Purpose
The Orchestrator ensures that changes across multiple components (backend, frontend, database, tests) are cohesive, consistent, and follow the project's architectural patterns.

## 📋 Feature Completeness Checklist

**Backend Implementation**
- [ ] New models defined in `app/models.py` with proper type hints
- [ ] Database migrations created (if schema changes)
- [ ] API endpoints in `app/main.py` with proper error handling
- [ ] Input validation using Pydantic schemas
- [ ] Unit tests for business logic
- [ ] Integration tests for API endpoints

**Frontend Implementation**
- [ ] TypeScript components with strict types (no `any`)
- [ ] Props interfaces properly defined
- [ ] State management implemented (Context API)
- [ ] UI components follow Tailwind patterns
- [ ] Unit tests with React Testing Library
- [ ] API integration with proper error handling

**Testing Coverage**
- [ ] Backend: minimum 80% coverage
- [ ] Frontend: minimum 80% coverage
- [ ] E2E tests for critical user flows

**Security Review**
- [ ] No hardcoded secrets or credentials
- [ ] Input validation on both frontend and backend
- [ ] Authentication/authorization properly implemented
- [ ] SQL injection prevention (using ORM)

## 🎯 Pre-PR Integration Checklist
- [ ] `pre-commit run --all-files` passes
- [ ] All tests pass: pytest + npm test
- [ ] New tests added for new functionality
- [ ] Coverage didn't decrease
- [ ] Commits follow Conventional Commits format
- [ ] PR description clearly explains changes