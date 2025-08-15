Before you start, read and follow `docs/MASTER_PROMPT.md` and `docs/ARCHITECTURE.md`. Produce a minimal diff + tests.

## Task 1 – Production-grade Streamlit Chat UI (EN/PL, resilient UX)
**Files:** `ui/app.py`, `ui/helpers.py`, `ui/tests/test_ui_helpers.py`, `i18n/en.json`, `i18n/pl.json`
**Scope:** session_state chat history; send last N turns to `/proxy`; sidebar model/max_tokens/lang; clear chat; error banners; escape content; 8k clamp; streaming-ready boundary.
**API:** POST `{GP_API_BASE}/proxy` with `{model,max_tokens,messages[]}`; returns `{conversation_id, reply, usage?}`.
**Tests:** helpers (trim history, payload shaping, i18n lookup), snapshot simple render; mock HTTP.
**Commands:** see PR body; `pytest -q`; `streamlit run ui/app.py`.
**Notes:** env `GP_API_BASE`, `DEFAULT_MODEL`, `MAX_TOKENS`, `HISTORY_MAX_TURNS`. No migrations.
