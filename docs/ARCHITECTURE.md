# GuardPilot Architecture (High-Level)

## Purpose
On-prem proxy to capture all LLM interactions, detect PII & Annex III risk, store immutable logs, and present a secure dashboard with exportable Annex IV PDFs.

## Components
- **Caddy (TLS/OIDC/Proxy)** → routes `/api/*` to FastAPI; `/` to Streamlit.
- **FastAPI backend** (`backend/app/`):
  - `/proxy` – forwards chat to LLM, runs PII & risk detection, writes DB + Parquet hash chain.
  - `/logs`, `/risk_incidents` – retrieval; later: search/pagination.
  - `/integrity` – verifies hash chain (Task 3).
  - `/export/*` – WeasyPrint PDFs (Task 6).
  - `/health`, `/ready`, `/metrics`.
- **Streamlit UI** (`ui/app.py`):
  - Chat (multi-turn; EN/PL).
  - Logs/Incidents view with filters/masking.
  - Export PDF action.
- **PostgreSQL** – searchable store of conversation logs.
- **Parquet + hash chain** – immutable, append-only log with tamper evidence.

## Data Model (MVP)
`ConversationLog` (id, conversation_id, ts, user_id?, model, prompt, response, risk_level, tags[], pii_detected, detected_pii[], parquet_file, hash_ptr, ...).

## Flow
Client → Caddy → FastAPI `/proxy`:
1. Validate input, clamp sizes.
2. Call LLM (or echo mode if no API key).
3. PII + risk detection; send alerts if needed.
4. Persist to Postgres; append to Parquet; update hash chain.
5. Return reply (+ usage if available).

## i18n
`i18n/en.json`, `i18n/pl.json`; helpers in backend & UI; parity checker in CI.

## Security Defaults
TLS via Caddy, BasicAuth (dev), OIDC (prod). Least privilege Docker, rate limits, structured logs, no secret/PII logging.
