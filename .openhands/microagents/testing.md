---
name: testing-guidelines
triggers:
  - test
  - testing
  - pytest
  - vitest
  - playwright
  - coverage
---

# Testing Guidelines

## 🎯 Coverage Targets
- **Backend**: Minimum 80% coverage (pytest)
- **Frontend**: Minimum 80% coverage (Vitest)
- **E2E**: Critical user flows (Playwright)

## 🐍 Backend Tests (pytest)
- Structure: unit/, integration/, fixtures.py
- Running: `pytest`, `pytest -v --cov`

## ⚛️ Frontend Tests (Vitest)
- Location: `src/__tests__/`
- Running: `npm test`, `npm test -- --coverage`

## 🎭 E2E Tests (Playwright)
- Location: `playwright-tests/`
- Running: `npx playwright test`

## 🎨 Best Practices
- Test behavior, not implementation
- Use descriptive test names
- Follow AAA pattern (Arrange-Act-Assert)
- Mock external APIs
- Test error cases