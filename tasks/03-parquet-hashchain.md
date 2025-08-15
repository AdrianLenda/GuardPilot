Before you start, read and follow `docs/MASTER_PROMPT.md` and `docs/ARCHITECTURE.md`. Produce a minimal diff + tests.

## Task 3 – Parquet rotation + hash-chain verification
**Files:** `backend/app/utils/parquet_logger.py`, `backend/app/main.py` (add `/integrity`), `backend/tests/test_parquet_chain.py`
**Scope:** `LOGS_DIR` default `data`; rotate daily `YYYY-MM-DD.parquet` + `YYYY-MM-DD.hashlog`; verify_chain() returns (ok, break_index); JSON log per append.
**API:** `GET /integrity` → `{"ok": true, "break_index": null, "file": "YYYY-MM-DD.parquet"}`.
**Tests:** append N → ok; corrupt ledger → fail.
**Commands:** `pytest -q`; `uvicorn ...`; `curl /integrity`.
**Notes:** No migrations.
