# Modules & Responsibilities
- **backend/app/main.py** – FastAPI app, routes, dependency wiring.
- **backend/app/models.py** – SQLModel definitions.
- **backend/app/database.py** – DB engine, session, init.
- **backend/app/utils/** – `pii_detection.py`, `risk_classifier.py`, `parquet_logger.py`, i18n helper.
- **ui/app.py** – Streamlit UI (Chat + Logs).
- **ui/helpers.py** – client utils (i18n, payload shaping, trimming).
- **infra/docker-compose.yml** – services; add Mailhog (dev).
- **Caddyfile** – TLS/proxy/auth.
