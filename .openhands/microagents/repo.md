# GuardPilot - Project Guidelines

## 📋 Project Description
GuardPilot is an on-premise security monitoring platform with FastAPI backend and React frontend.

## 🏗️ Architecture
- **Backend**: Python 3.11+ + FastAPI + SQLModel + PostgreSQL
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Deployment**: Docker + GitHub Actions
- **Database**: PostgreSQL (production) or SQLite (dev)

## 🚀 Quick Start
```bash
./dev.sh       # backend only
./dev.sh -u    # backend + UI
```

## ✅ Before Committing
1. Run: `pre-commit run --all-files`
2. Check: Backend tests (pytest), Frontend tests (npm test)
3. Format: Black, Ruff, Prettier automatically applied

## 📝 Commit Message Convention
Using Conventional Commits:
- `feat: description` - new feature
- `fix: description` - bug fix
- `test: description` - new tests

## 🔐 Security
- DO NOT commit: API keys, passwords, tokens, personal data
- Gitleaks automatically scans staged files