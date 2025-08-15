# GuardPilot – MASTER PROMPT (Repo Rules)

You are my implementation agent for **AdrianLenda/GuardPilot**.

## Repository & Branching
- Backend (API): `backend/app/...`
- Frontend (UI): `ui/app.py` (+ helpers `ui/helpers.py`, tests `ui/tests/`)
- Infra: `infra/docker-compose.yml`, `Caddyfile`
- Migrations: `backend/alembic/` (introduce as needed)
- Default PR target: **`dev`** (I will promote to `mainn`)
- **PR size**: ≤ **300–500 LOC** including tests. If larger, **split** (e.g., API+tests then UI).

## Output required for every task/PR
1) **Plan** – files to add/change.
2) **Unified diff** – only relevant files (minimal diff).
3) **Commands** – how I run lint/tests/smoke locally.
4) **Notes** – env vars, migrations (up/down), rollout/rollback.

## Definition of Done (enforced by CI)
- Lint/format: **ruff**, **black --check**.
- Tests: **pytest green**, **coverage ≥ 70%** (raise later).
- i18n: **EN/PL key parity** check must pass; fallback to EN implemented.
- (Optional) mypy – add gradually.
- **No secrets in code**; `.env` ignored; use repo/Codespaces secrets only.
- **OpenAI is mocked in tests**; local dev supports echo mode when `OPENAI_API_KEY` is unset.
- If schema changes: **Alembic migration** (up/down) + rollback plan in PR notes.

## Security & Privacy
- Validate inputs; clamp body size (~256KB) and message length (~8k).
- Timeouts; map OpenAI errors: **429/502/504** → friendly UI messages.
- Rate limiting (per IP/user).
- **Never log secrets or raw PII**; mask PII in logs/emails/UI; store hashes where viable.
- Structured **JSON logs**; include `request_id` (correlate UI↔API).
- Auth: Dev = BasicAuth (Caddy). Prod = **OIDC** (Caddy/Authlib). Roles: user/auditor/admin.

## Internationalization
- Start with **EN/PL** for UI & PDFs.
- Fallback to EN; **parity test** blocks CI on key drift.

## Observability
- `/health` + `/ready` endpoints.
- `/metrics` (Prometheus) guarded or localhost.
- Indexes in DB for `ts`, `risk_level`, and FTS `tsvector`.

## Workflow
- One feature = one PR. Minimal diffs, only relevant files.
- After generation: apply diff → run dev script/compose → `curl /health` → `pytest -q` → review → merge to `dev`.
- If CI fails, provide logs with the instruction: **“fix failing tests & update PR.”**
