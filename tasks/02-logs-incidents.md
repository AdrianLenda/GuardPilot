Before you start, read and follow `docs/MASTER_PROMPT.md` and `docs/ARCHITECTURE.md`. Produce a minimal diff + tests.

## Task 2 – Logs & Incidents Dashboard (filters, masking, drill-down)
**Files:** `ui/app.py`, `ui/helpers.py`, `ui/tests/test_ui_helpers.py`, `backend/tests/test_incidents_subset.py`
**Scope:** Tabs ["Chat","Logs"]; table from `/logs`; toggle "Incidents only" → `/risk_incidents`; expander with full details + masked PII; export PDF button (hide if 404); client filters (risk, date, query); client pagination; roles hook.
**Security:** mask emails & PESEL/NIP in UI; never show raw PII to non-auditors.
**Tests:** `/risk_incidents ⊆ /logs` (backend test); helpers for masking & pagination.
**Commands:** `pytest -q`; `streamlit run ui/app.py`.
**Notes:** No migrations.
