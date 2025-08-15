# ADR 0002 – Immutable Logging (Parquet + Hash Chain)
**Status:** Accepted  
**Context:** Logs must be tamper-evident (Annex IV).  
**Decision:** Append conversation rows to daily Parquet files and maintain a SHA-256 link ledger (prev_hash + serialized_record). Provide `/integrity` to verify.  
**Consequences:** Detects post-hoc changes. Requires rotation, careful append semantics, and verification tooling.
