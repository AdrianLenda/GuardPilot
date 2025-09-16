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
