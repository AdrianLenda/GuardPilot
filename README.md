# GuardPilot

This repository contains the on-premise codebase for **GuardPilot**, including a FastAPI backend, React/Streamlit front-end and infrastructure for local deployment.

## Day-1 End-to-End Setup

To bootstrap the system on a developer machine, run the provided `dev.sh` script from the project root. This script creates a Python virtual environment, installs dependencies, brings up Postgres and other services via Docker Compose, and runs the backend (and the UI if the `-u` flag is provided).

```bash
./dev.sh       # backend only
./dev.sh -u    # backend + UI (Streamlit or React)
```

Before running, copy `.env.sample` to `.env` and update any secrets such as `OPENAI_API_KEY` and `DATABASE_URL`. The default `.env.sample` uses a local SQLite database; for production specify your Postgres URI, for example:

```env
DATABASE_URL=postgresql+psycopg://guardpilot:guardpilot@db:5432/guardpilot
```

## Verifying the API

Once the server is running, you can verify the key endpoints via `curl`:

### Health check
```bash
curl -s http://localhost:8000/health
```

### Proxy endpoint
```bash
curl -s -X POST http://localhost:8000/proxy \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}'
```

### Logs endpoint
```bash
curl -s "http://localhost:8000/logs?limit=10"
```

Each call should return a JSON object. The `/proxy` endpoint will proxy your prompt through the configured LLM provider and persist a masked log entry; `/logs` returns the most recent conversation logs.

## Database Migration Rollback

The project uses Alembic for schema migrations. To roll back the most recent migration during development, run:

```bash
alembic downgrade -1
```

If you want to back up the database before migrating or rolling back, you can create a SQL dump using:

```bash
pg_dump --no-owner --file backup.sql "$DATABASE_URL"
```

See `sops.md` for detailed backup/restore procedures and other operational considerations.


## Pre-commit Hooks

This repository uses [pre-commit](https://pre-commit.com/) to automate code quality checks before each commit. After cloning the repository, install the hooks with:

```bash
pip install pre-commit
pre-commit install
```

This installs Git hooks that will run `ruff` (linting), `black` (formatting), `mypy` (type checking), `eslint`/`prettier` (for the JavaScript/TypeScript code) and `gitleaks` (secret scanning) on the staged files. To run all hooks against the entire repository, run:

```bash
pre-commit run --all-files
```

## Continuous Integration (CI)

GitHub Actions workflows enforce the same checks in CI. The workflows live under `.github/workflows/` and are triggered on pushes and pull requests:

- **backend.yml** – Sets up Python, installs dependencies, runs `ruff`/`black`/`mypy`, and executes the backend test suite (`pytest`).
- **frontend.yml** – Sets up Node.js, runs `npm ci` to install dependencies, lints the front‑end code with ESLint/Prettier, and runs unit tests via `npm test` (Vitest).
- **Playwright smoke test** – A Playwright configuration (`playwright.config.ts`) and test (`playwright-tests/home.spec.ts`) provide a simple end‑to‑end check that the React app starts and renders the expected title. This test runs in its own workflow.

CI must pass before merging changes into the main branch.
